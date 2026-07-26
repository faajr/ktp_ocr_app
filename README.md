# AI KTP Classification & OCR (OpenRouter + Streamlit)

Aplikasi contoh untuk Final Project: klasifikasi dokumen + OCR menggunakan AI Vision (OpenRouter),
validasi dengan business rule, penyimpanan ke database, dan dashboard Streamlit.

## 📁 Struktur File

```
ktp_ocr_app/
├── app.py                 # Aplikasi utama Streamlit (dashboard)
├── openrouter_client.py   # Komunikasi ke OpenRouter Vision API (klasifikasi & OCR)
├── validation.py          # Business rule validation untuk data KTP
├── database.py            # Penyimpanan & pembacaan data pakai SQLite
├── test_klasifikasi.py    # Script untuk testing akurasi klasifikasi (min. 20 gambar)
├── requirements.txt       # Daftar library yang dibutuhkan
├── .env.example           # Contoh isi file .env
└── README.md
```

Setiap file punya 1 tanggung jawab saja (biar mudah dipelajari dan dikembangkan):
- `openrouter_client.py` → ngobrol dengan AI
- `validation.py` → cek aturan bisnis
- `database.py` → simpan/baca data
- `app.py` → tampilan & menghubungkan semuanya

## 🚀 Cara Menjalankan

### 1. Install Python (jika belum ada)
Pastikan Python 3.9 ke atas sudah terinstall.

### 2. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install semua library
```bash
pip install -r requirements.txt
```

### 4. Siapkan API Key OpenRouter
1. Salin file `.env.example` menjadi `.env`
2. Isi `OPENROUTER_API_KEY` dengan API key OpenRouter kamu (kamu sudah punya ini)
3. (Opsional) Ganti `OPENROUTER_MODEL` kalau ingin pakai model lain yang mendukung gambar

```
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
OPENROUTER_MODEL=openrouter/free
```

> Catatan: `openrouter/free` otomatis memilih model gratis yang mendukung gambar.
> Kalau hasil OCR kurang akurat, coba ganti ke model vision spesifik (cek daftar model
> yang mendukung gambar di https://openrouter.ai/models — filter "Input modalities: image").

### 5. Jalankan aplikasi
```bash
streamlit run app.py
```
Aplikasi akan terbuka otomatis di browser (testing awal dilakukan di url `http://localhost:8501`).

## 🧪 Testing awal (Tahap 8)

1. Buat folder `test_images/` di dalam folder project ini
2. Masukkan minimal 20 gambar (campuran KTP dan bukan KTP)
3. Buat file `test_images/label.csv` berisi:
   ```csv
   filename,expected
   ktp1.jpg,KTP
   sim1.jpg,Bukan KTP
   motor1.jpg,Bukan KTP
   ```
4. Jalankan:
   ```bash
   python test_klasifikasi.py
   ```
5. Hasil & akurasi akan tersimpan otomatis di `hasil_testing.csv`

## ☁️ Deployment

### Streamlit Community Cloud
1. Push folder project ke GitHub
2. Buka https://share.streamlit.io, hubungkan ke repo GitHub kamu
3. Di menu "Secrets", tambahkan:
   ```
   OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxx"
   OPENROUTER_MODEL = "openrouter/free"
   ```
4. Deploy
