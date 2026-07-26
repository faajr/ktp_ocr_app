import sqlite3
import json
from datetime import datetime

DB_NAME = "ktp_data.db"


def init_db():
    """
    Membuat tabel 'ktp_records' jika belum ada.
    Dipanggil sekali di awal aplikasi (lihat app.py).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ktp_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            nomor_dokumen TEXT,
            jenis_dokumen TEXT,
            tanggal_upload TEXT,
            status_validasi TEXT,
            data_ocr_json TEXT,
            detail_validasi_json TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def save_record(ocr_data: dict, status_validasi: str, detail_validasi: dict, jenis_dokumen: str = "KTP"):
    """
    Menyimpan 1 hasil OCR ke database.

    Parameter:
        ocr_data (dict)         : hasil ekstraksi OCR, misalnya {"nama": "Andi", "nik": "..."}
        status_validasi (str)   : "VALID" atau "INVALID"
        detail_validasi (dict)  : rincian validasi tiap field
        jenis_dokumen (str)     : jenis dokumen, default "KTP"
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ktp_records
            (nama, nomor_dokumen, jenis_dokumen, tanggal_upload, status_validasi, data_ocr_json, detail_validasi_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ocr_data.get("nama", ""),
            ocr_data.get("nik", ""),
            jenis_dokumen,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status_validasi,
            json.dumps(ocr_data, ensure_ascii=False),
            json.dumps(detail_validasi, ensure_ascii=False),
        ),
    )

    conn.commit()
    conn.close()


def get_all_records():
    """
    Mengambil semua data yang tersimpan, diurutkan dari yang terbaru.
    Mengembalikan list of dict supaya mudah ditampilkan di Streamlit.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # supaya hasil query bisa diakses seperti dict
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ktp_records ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def delete_record(record_id: int):
    """Menghapus 1 baris data berdasarkan id (opsional, untuk kebutuhan koreksi data)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ktp_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def get_record_by_id(record_id: int):
    """Mengambil 1 data berdasarkan ID. Mengembalikan dict atau None."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ktp_records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_statistics():
    """
    Menghitung statistik ringkasan dari database.
    Mengembalikan dict: {"total": int, "valid": int, "invalid": int}
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM ktp_records")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ktp_records WHERE status_validasi = 'VALID'")
    valid = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ktp_records WHERE status_validasi = 'INVALID'")
    invalid = cursor.fetchone()[0]

    conn.close()
    return {"total": total, "valid": valid, "invalid": invalid}

