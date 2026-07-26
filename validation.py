from datetime import datetime


def _parse_tanggal_lahir_dari_nik(nik: str):
    """
    Mengambil tanggal lahir & jenis kelamin dari 6 digit NIK (digit ke-7 s/d ke-12).
    Mengembalikan (tanggal_lahir: datetime | None, jenis_kelamin: str | None).
    """
    digit_tanggal = nik[6:8]
    digit_bulan = nik[8:10]
    digit_tahun = nik[10:12]

    try:
        hari = int(digit_tanggal)
        bulan = int(digit_bulan)
        tahun_yy = int(digit_tahun)
    except ValueError:
        return None, None

    # Jika hari > 40, berarti perempuan (aturan resmi NIK Indonesia)
    if hari > 40:
        jenis_kelamin = "PEREMPUAN"
        hari -= 40
    else:
        jenis_kelamin = "LAKI-LAKI"

    # Menentukan abad: kalau 2 digit tahun <= 2 digit tahun sekarang -> anggap 2000-an
    tahun_sekarang_yy = datetime.now().year % 100
    tahun_penuh = 2000 + tahun_yy if tahun_yy <= tahun_sekarang_yy else 1900 + tahun_yy

    try:
        tanggal_lahir = datetime(tahun_penuh, bulan, hari)
    except ValueError:
        return None, None

    return tanggal_lahir, jenis_kelamin


def validate_ktp(data: dict) -> dict:
    """
    Menjalankan semua business rule untuk 1 hasil OCR KTP.

    Parameter:
        data (dict): hasil OCR, contoh:
            {
                "nik": "3275xxxxxxxxxxxx",
                "nama": "Andi",
                "jenis_kelamin": "LAKI-LAKI",
                "tempat_tgl_lahir": "Jakarta, 17-08-1995",
                "berlaku_hingga": "SEUMUR HIDUP",
                ...
            }

    Mengembalikan dict berisi status per-field + status keseluruhan, contoh:
        {
            "status_keseluruhan": "VALID" atau "INVALID",
            "detail": {
                "nik_panjang": {"status": "VALID", "pesan": "..."},
                "nik_angka": {"status": "VALID", "pesan": "..."},
                ...
            }
        }
    """
    detail = {}
    nik = str(data.get("nik", "")).strip()

    # 1. Panjang NIK harus 16 digit
    if len(nik) == 16:
        detail["nik_panjang"] = {"status": "VALID", "pesan": "Panjang NIK 16 digit"}
    else:
        detail["nik_panjang"] = {
            "status": "INVALID",
            "pesan": f"Panjang NIK {len(nik)} digit, seharusnya 16 digit",
        }

    # 2. NIK hanya boleh berisi angka
    if nik.isdigit():
        detail["nik_angka"] = {"status": "VALID", "pesan": "NIK hanya berisi angka"}
    else:
        detail["nik_angka"] = {"status": "INVALID", "pesan": "NIK mengandung karakter selain angka"}

    # Kalau NIK tidak 16 digit angka, tanggal lahir & gender dari NIK tidak bisa dihitung.
    # Sisanya otomatis INVALID biar tidak error.
    if detail["nik_panjang"]["status"] == "VALID" and detail["nik_angka"]["status"] == "VALID":
        tanggal_lahir_nik, gender_nik = _parse_tanggal_lahir_dari_nik(nik)
    else:
        tanggal_lahir_nik, gender_nik = None, None

    # 3. Validasi tanggal lahir dari NIK bisa di-parse dengan benar
    if tanggal_lahir_nik is not None:
        detail["tanggal_lahir_nik"] = {
            "status": "VALID",
            "pesan": f"Tanggal lahir sesuai NIK: {tanggal_lahir_nik.strftime('%d-%m-%Y')}",
        }
    else:
        detail["tanggal_lahir_nik"] = {"status": "INVALID", "pesan": "Tanggal lahir pada NIK tidak valid"}

    # 4. Validasi jenis kelamin berdasarkan NIK vs hasil OCR field jenis_kelamin
    jenis_kelamin_ocr = str(data.get("jenis_kelamin", "")).strip().upper()
    if gender_nik is not None:
        if jenis_kelamin_ocr and jenis_kelamin_ocr == gender_nik:
            detail["jenis_kelamin"] = {"status": "VALID", "pesan": "Jenis kelamin sesuai dengan NIK"}
        else:
            detail["jenis_kelamin"] = {
                "status": "INVALID",
                "pesan": f"Jenis kelamin OCR ('{jenis_kelamin_ocr}') tidak sesuai NIK (harusnya '{gender_nik}')",
            }
    else:
        detail["jenis_kelamin"] = {"status": "INVALID", "pesan": "Tidak bisa dicek, NIK tidak valid"}

    # 5. Validasi format tanggal lahir yang tertulis di field tempat_tgl_lahir (kalau ada)
    #    Kita hanya cek apakah field ini terisi dan tanggal dari NIK ada di dalamnya.
    tempat_tgl_lahir_ocr = str(data.get("tempat_tgl_lahir", "")).strip()
    if tanggal_lahir_nik is not None and tempat_tgl_lahir_ocr:
        tanggal_str_1 = tanggal_lahir_nik.strftime("%d-%m-%Y")
        tanggal_str_2 = tanggal_lahir_nik.strftime("%d/%m/%Y")
        if tanggal_str_1 in tempat_tgl_lahir_ocr or tanggal_str_2 in tempat_tgl_lahir_ocr:
            detail["format_tanggal"] = {"status": "VALID", "pesan": "Tanggal lahir di KTP cocok dengan NIK"}
        else:
            detail["format_tanggal"] = {
                "status": "INVALID",
                "pesan": f"Tanggal lahir di KTP tidak cocok dengan NIK (harusnya mengandung {tanggal_str_1})",
            }
    else:
        detail["format_tanggal"] = {"status": "INVALID", "pesan": "Field tempat_tgl_lahir kosong atau tidak bisa dicek"}

    # 6. Validasi status berlaku (SEUMUR HIDUP atau tanggal yang belum kadaluarsa)
    berlaku_hingga = str(data.get("berlaku_hingga", "")).strip().upper()
    if berlaku_hingga == "SEUMUR HIDUP":
        detail["masa_berlaku"] = {"status": "VALID", "pesan": "Berlaku seumur hidup"}
    else:
        tanggal_valid = None
        for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
            try:
                tanggal_valid = datetime.strptime(berlaku_hingga, fmt)
                break
            except ValueError:
                continue

        if tanggal_valid is None:
            detail["masa_berlaku"] = {
                "status": "INVALID",
                "pesan": "Format 'berlaku_hingga' tidak dikenali (harus SEUMUR HIDUP atau DD-MM-YYYY)",
            }
        elif tanggal_valid >= datetime.now():
            detail["masa_berlaku"] = {"status": "VALID", "pesan": "KTP masih berlaku"}
        else:
            detail["masa_berlaku"] = {"status": "INVALID", "pesan": "KTP sudah kadaluarsa"}

    # Status keseluruhan: VALID hanya jika SEMUA field di atas VALID
    semua_valid = all(item["status"] == "VALID" for item in detail.values())

    return {
        "status_keseluruhan": "VALID" if semua_valid else "INVALID",
        "detail": detail,
    }
