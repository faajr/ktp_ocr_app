"""
openrouter_client.py
---------------------
Modul ini bertugas berkomunikasi dengan OpenRouter Vision API untuk 2 tugas:
    1. classify_image()  -> menentukan apakah gambar adalah KTP atau bukan
    2. extract_ocr()     -> membaca isi KTP dan mengembalikan data dalam JSON

Kenapa pakai OpenRouter?
    OpenRouter menyediakan 1 API yang bisa dipakai untuk banyak model AI
    (termasuk model yang punya kemampuan "vision" / membaca gambar),
    jadi kita tidak perlu daftar ke banyak provider berbeda.

Catatan penting:
    - Tidak ada Regex dipakai untuk membaca isi dokumen (sesuai instruksi project).
    - Semua pembacaan teks dari gambar dilakukan oleh AI (model vision), bukan library OCR biasa.
"""

import base64
import json
import os
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _encode_image_to_base64(image_bytes: bytes) -> str:
    """Mengubah gambar (bytes) menjadi string base64, format yang dibutuhkan API."""
    return base64.b64encode(image_bytes).decode("utf-8")


class OpenRouterError(Exception):
    """Dilempar kalau OpenRouter membalas dengan error atau jawaban kosong."""
    pass


def _call_openrouter_vision_sekali(image_bytes: bytes, prompt: str, api_key: str, model: str) -> str:
    """
    Satu kali percobaan mengirim gambar + prompt ke OpenRouter.
    Melempar OpenRouterError kalau ada masalah, supaya pemanggil bisa memutuskan retry atau tidak.
    """
    base64_image = _encode_image_to_base64(image_bytes)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)

    # Coba parse JSON balasan dulu, sebelum raise_for_status(), karena
    # OpenRouter sering mengirim detail error yang berguna di body JSON-nya.
    try:
        hasil = response.json()
    except ValueError:
        response.raise_for_status()
        raise OpenRouterError(f"Balasan OpenRouter bukan JSON valid: {response.text[:300]}")

    # Kasus 1: OpenRouter mengembalikan field "error" (misalnya rate limit, model tidak tersedia, dsb)
    if "error" in hasil:
        pesan_error = hasil["error"].get("message", str(hasil["error"]))
        raise OpenRouterError(f"OpenRouter error: {pesan_error}")

    response.raise_for_status()

    choices = hasil.get("choices", [])
    if not choices:
        raise OpenRouterError("Balasan OpenRouter tidak berisi 'choices' sama sekali.")

    pilihan = choices[0]
    alasan_berhenti = pilihan.get("finish_reason", "")
    konten = pilihan.get("message", {}).get("content", "")

    # Kasus 2: model menolak / difilter oleh content moderation -> konten kosong
    if not konten or not konten.strip():
        if alasan_berhenti == "content_filter":
            raise OpenRouterError(
                "Model menolak memproses gambar ini (kena content filter). "
                "Coba ganti OPENROUTER_MODEL di file .env ke model vision lain."
            )
        raise OpenRouterError(
            f"Model mengembalikan jawaban kosong (finish_reason='{alasan_berhenti}'). "
            "Model yang dipakai kemungkinan tidak konsisten mendukung gambar. "
            "Coba ganti OPENROUTER_MODEL di file .env ke model vision spesifik "
            "(bukan 'openrouter/free' yang memilih model secara acak)."
        )

    return konten


def _call_openrouter_vision(image_bytes: bytes, prompt: str, api_key: str, model: str) -> str:
    """
    Fungsi dasar untuk mengirim gambar + prompt teks ke OpenRouter,
    lalu mengembalikan jawaban teks dari AI.

    Otomatis mencoba ULANG SEKALI kalau percobaan pertama gagal/kosong —
    berguna terutama kalau model="openrouter/free" (router bisa memilih
    model acak yang berbeda di percobaan kedua).

    Fungsi ini dipakai bersama oleh classify_image() dan extract_ocr(),
    supaya tidak ada kode yang diulang-ulang (DRY principle).
    """
    error_terakhir = None

    for percobaan in range(2):  # coba maksimal 2 kali
        try:
            return _call_openrouter_vision_sekali(image_bytes, prompt, api_key, model)
        except OpenRouterError as e:
            error_terakhir = e
            continue
        except requests.exceptions.RequestException as e:
            error_terakhir = OpenRouterError(f"Gagal menghubungi OpenRouter: {e}")
            continue

    # Kalau 2 percobaan tetap gagal, lempar error terakhir supaya
    # pemanggil (classify_image / extract_ocr) tahu ada masalah nyata.
    raise error_terakhir


def _extract_json_from_text(text: str) -> dict:
    """
    AI kadang membalas dengan teks tambahan di luar JSON (misalnya penjelasan
    atau ```json ... ```). Fungsi ini mengambil bagian JSON-nya saja.
    """
    text = text.strip()

    # Buang pembungkus markdown ```json ... ``` kalau ada
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    # Ambil teks dari kurung kurawal pertama sampai kurung kurawal terakhir
    awal = text.find("{")
    akhir = text.rfind("}")
    if awal != -1 and akhir != -1:
        text = text[awal : akhir + 1]

    return json.loads(text)


def classify_image(image_bytes: bytes, api_key: str, model: str) -> dict:
    """
    Tahap 1: Klasifikasi gambar, apakah ini KTP Indonesia atau bukan.

    Return contoh:
        {"is_ktp": True}
        atau
        {"is_ktp": False}
    """
    prompt = (
        "Apakah gambar ini merupakan KTP (Kartu Tanda Penduduk) Indonesia yang asli? "
        "Jawab HANYA dalam format JSON tanpa penjelasan tambahan, contoh: "
        '{"is_ktp": true} atau {"is_ktp": false}'
    )

    try:
        teks_jawaban = _call_openrouter_vision(image_bytes, prompt, api_key, model)
    except OpenRouterError as e:
        return {"is_ktp": False, "error": str(e)}

    try:
        hasil_json = _extract_json_from_text(teks_jawaban)
        # Pastikan key "is_ktp" selalu ada dan bertipe bool
        return {"is_ktp": bool(hasil_json.get("is_ktp", False))}
    except (json.JSONDecodeError, ValueError):
        # Kalau AI tidak menjawab format JSON yang valid, anggap saja bukan KTP
        # supaya proses berhenti dengan aman (fail-safe), bukan crash.
        return {"is_ktp": False}


def extract_ocr(image_bytes: bytes, api_key: str, model: str) -> dict:
    """
    Tahap 2: OCR menggunakan AI Vision. Membaca semua field penting dari KTP
    dan mengembalikan dalam bentuk dict (siap divalidasi & disimpan ke database).
    """
    prompt = """Kamu adalah sistem OCR untuk KTP Indonesia.
Baca gambar KTP berikut dan ekstrak informasinya.
Jawab HANYA dalam format JSON persis seperti struktur di bawah ini, tanpa penjelasan tambahan.
Jika ada field yang tidak terbaca, isi dengan string kosong "".

{
  "nik": "",
  "nama": "",
  "tempat_tgl_lahir": "",
  "jenis_kelamin": "",
  "agama": "",
  "alamat": "",
  "rt": "",
  "rw": "",
  "kelurahan": "",
  "kecamatan": "",
  "status_perkawinan": "",
  "pekerjaan": "",
  "kewarganegaraan": "",
  "berlaku_hingga": ""
}

Ketentuan pengisian:
- "jenis_kelamin" harus persis "LAKI-LAKI" atau "PEREMPUAN" (huruf kapital)
- "berlaku_hingga" diisi "SEUMUR HIDUP" atau tanggal format DD-MM-YYYY
"""

    try:
        teks_jawaban = _call_openrouter_vision(image_bytes, prompt, api_key, model)
        
        # Check if model returned a safety warning or empty response
        if not teks_jawaban.strip() or "User Safety: unsafe" in teks_jawaban:
            return {"error": f"Model menolak memproses gambar karena alasan keamanan (Safety Filter). Jawaban AI:\n{teks_jawaban}"}
            
    except OpenRouterError as e:
        # Ini kasus yang bikin error "Expecting value: line 1 column 1" sebelumnya —
        # sekarang pesannya jelas ("model kosong", "kena content filter", dll),
        # bukan sekadar gagal parse JSON dari string kosong.
        return {"error": str(e)}

    try:
        return _extract_json_from_text(teks_jawaban)
    except (json.JSONDecodeError, ValueError) as e:
        # Kembalikan dict kosong + pesan error, serta teks mentah dari AI
        return {"error": f"Gagal membaca hasil OCR sebagai JSON.\nJawaban AI:\n{teks_jawaban}"}
