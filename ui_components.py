import streamlit as st
import textwrap

def inject_custom_css():
    """
    Fungsi ini digunakan untuk menyuntikkan (inject) CSS kustom ke dalam aplikasi Streamlit.
    CSS ini akan mengubah tampilan bawaan Streamlit menjadi lebih premium dan modern dengan efek glassmorphism.
    """
    css = textwrap.dedent("""\
    <style>
    /* Mengimpor font Inter dari Google Fonts untuk tampilan yang lebih modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Terapkan font Inter ke semua elemen dan atur warna teks bawaan */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #e0e0e0 !important;
    }

    /* Mengubah background utama aplikasi menjadi gradien gelap */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
        background-attachment: fixed !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Styling untuk Sidebar dengan efek transparan (glassmorphism) */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(0, 210, 255, 0.2) !important;
        box-shadow: 2px 0 15px rgba(0, 210, 255, 0.1) !important;
    }
    
    /* Hover effect untuk radio button di sidebar */
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 15px !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    /* Glassmorphism Card (Kartu Transparan) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 210, 255, 0.2);
        border: 1px solid rgba(0, 210, 255, 0.3);
    }

    /* Styling tombol utama Streamlit */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3) !important;
    }
    [data-testid="baseButton-primary"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.5) !important;
    }

    /* Indikator Progres Langkah (Step Progress) */
    .step-progress {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 40px 0;
        position: relative;
    }
    .step-progress::before {
        content: "";
        position: absolute;
        top: 25px;
        left: 0;
        right: 0;
        height: 3px;
        background: rgba(255, 255, 255, 0.1);
        z-index: 1;
    }
    .step-item {
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        width: 60px;
    }
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #24243e;
        border: 2px solid rgba(255, 255, 255, 0.2);
        font-size: 20px;
        margin-bottom: 10px;
        transition: all 0.4s ease;
    }
    .step-label {
        font-size: 12px;
        font-weight: 500;
        color: #a0a0a0;
    }
    .step-done .step-circle {
        background: #28a745;
        border-color: #28a745;
        color: white;
    }
    .step-done .step-label {
        color: #28a745;
    }
    .step-active .step-circle {
        border-color: #00d2ff;
        background: rgba(0, 210, 255, 0.1);
        color: #00d2ff;
        animation: pulse 2s infinite;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
    }
    .step-active .step-label {
        color: #00d2ff;
        font-weight: 700;
    }

    /* Badges (Label Validasi) */
    .badge {
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-valid {
        background: rgba(40, 167, 69, 0.2);
        color: #2ecc71;
        border: 1px solid rgba(40, 167, 69, 0.5);
    }
    .badge-invalid {
        background: rgba(220, 53, 69, 0.2);
        color: #ff4757;
        border: 1px solid rgba(220, 53, 69, 0.5);
    }

    /* Area Upload File */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(0, 210, 255, 0.4) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #00d2ff !important;
        background: rgba(0, 210, 255, 0.05) !important;
    }

    /* Animasi-animasi Kustom */
    @keyframes fadeInUp {
        0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 10px rgba(0, 210, 255, 0.3); }
        50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(0, 210, 255, 0.7); }
        100% { transform: scale(1); box-shadow: 0 0 10px rgba(0, 210, 255, 0.3); }
    }
    @keyframes slideIn {
        0% { transform: translateX(-20px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    .animate-slide-in {
        animation: slideIn 0.5s ease-out forwards;
    }

    /* Tabel Streamlit */
    [data-testid="stTable"] table {
        background-color: transparent !important;
        color: white !important;
    }
    [data-testid="stTable"] th {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #00d2ff !important;
    }
    [data-testid="stTable"] tr:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.02) !important;
    }
    [data-testid="stTable"] tr:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    /* Heading dan Text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* Metric Bawaan Streamlit */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
    }

    /* Alert / Pesan Status */
    [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-left: 4px solid #00d2ff !important;
        border-radius: 8px !important;
        color: white !important;
    }

    /* Kustomisasi Scrollbar untuk kecocokan tema */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0f0c29; 
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 210, 255, 0.3); 
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 210, 255, 0.6); 
    }
    </style>
    """)
    st.markdown(css, unsafe_allow_html=True)

def render_hero_section():
    """
    Menampilkan bagian Hero (header besar) di halaman utama dengan efek animasi.
    """
    hero_html = textwrap.dedent("""\
    <div class="glass-card animate-fade-in" style="text-align: center; padding: 40px 20px; margin-bottom: 30px;">
        <h1 style="font-size: 3rem; margin-bottom: 10px; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🪪 KTP OCR Intelligence</h1>
        <h3 style="color: #a0a0a0; font-weight: 400; margin-bottom: 20px;">AI-Powered Document Classification & OCR</h3>
        <p style="font-size: 1.1rem; color: #d0d0d0; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            Unggah gambar KTP Anda dan biarkan AI kami melakukan klasifikasi, mengekstrak data teks (OCR), dan memvalidasinya secara otomatis. 
            Cepat, akurat, dan canggih.
        </p>
    </div>
    """)
    st.markdown(hero_html, unsafe_allow_html=True)

def render_step_progress(current_step: int, total_steps: int = 6):
    """
    Menampilkan indikator langkah (step progress) secara horizontal.
    :param current_step: Langkah saat ini (1-index).
    :param total_steps: Total langkah yang ada.
    """
    steps_info = [
        {"label": "Upload", "icon": "☁️"},
        {"label": "Klasifikasi", "icon": "🤖"},
        {"label": "OCR", "icon": "📝"},
        {"label": "JSON Result", "icon": "{ }"},
        {"label": "Validasi", "icon": "✅"},
        {"label": "Database", "icon": "💾"}
    ]
    
    html = '<div class="step-progress animate-fade-in">'
    
    for i, step in enumerate(steps_info):
        step_num = i + 1
        
        # Menentukan status langkah (selesai, aktif, atau belum)
        if step_num < current_step:
            state_class = "step-done"
            icon = "✔️" # Ganti ikon jadi centang jika sudah selesai
        elif step_num == current_step:
            state_class = "step-active"
            icon = step["icon"]
        else:
            state_class = "step-pending"
            icon = step["icon"]
            
        html += (
            f'<div class="step-item {state_class}">'
            f'<div class="step-circle">{icon}</div>'
            f'<div class="step-label">{step["label"]}</div>'
            f'</div>'
        )
        
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def get_ocr_result_cards_html(ocr_data: dict) -> str:
    """
    Menghasilkan HTML hasil OCR dalam bentuk kartu (grid) untuk setiap kolom data.
    Lebih elegan dibandingkan dengan tabel biasa.
    :param ocr_data: Dictionary berisi pasangan kunci-nilai hasil OCR.
    :return: String HTML
    """
    html = '<div class="animate-fade-in" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px;">'
    
    for key, value in ocr_data.items():
        # Memformat key agar terlihat lebih rapi
        formatted_key = str(key).replace("_", " ").title()
        
        html += (
            '<div class="glass-card" style="padding: 15px;">'
            f'<div style="font-size: 0.8rem; color: #a0a0a0; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">{formatted_key}</div>'
            f'<div style="font-size: 1.1rem; color: #ffffff; font-weight: 500; word-break: break-word;">{value if value else "-"}</div>'
            '</div>'
        )
        
    html += '</div>'
    return html

def render_status_badge(status: str) -> str:
    """
    Membuat HTML untuk badge status.
    :param status: "VALID" atau "INVALID"
    :return: String HTML badge.
    """
    if status.upper() == "VALID":
        return '<span class="badge badge-valid">✓ VALID</span>'
    else:
        return '<span class="badge badge-invalid">✕ INVALID</span>'

def get_validation_table_html(detail: dict) -> str:
    """
    Menghasilkan HTML tabel hasil validasi dengan styling khusus.
    :param detail: Dictionary dari validation.py
    :return: String HTML
    """
    html = textwrap.dedent("""\
    <div style="overflow-x: auto; margin-top: 10px;">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.15);">
                    <th style="padding: 12px 15px; color: #00d2ff; font-weight: 600;">Rule Validasi</th>
                    <th style="padding: 12px 15px; color: #00d2ff; font-weight: 600; width: 120px;">Status</th>
                    <th style="padding: 12px 15px; color: #00d2ff; font-weight: 600;">Keterangan</th>
                </tr>
            </thead>
            <tbody>
    """)

    # detail adalah dict: {"nama_rule": {"status": "...", "pesan": "..."}, ...}
    for nama_rule, item in detail.items():
        status = item.get("status", "INVALID")
        pesan = item.get("pesan", "-")
        status_badge = render_status_badge(status)
        # Format nama rule agar lebih rapi (ganti underscore jadi spasi, capitalize)
        nama_tampil = nama_rule.replace("_", " ").title()

        html += (
            '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">'
            f'<td style="padding: 12px 15px; color: #e0e0e0;">{nama_tampil}</td>'
            f'<td style="padding: 12px 15px;">{status_badge}</td>'
            f'<td style="padding: 12px 15px; color: #b0b0b0; font-size: 0.9rem;">{pesan}</td>'
            '</tr>'
        )

    html += "</tbody></table></div>"
    return html

def render_stat_cards(total: int, valid: int, invalid: int):
    """
    Menampilkan 3 kartu statistik (Metric Cards) secara berdampingan.
    Digunakan di halaman Database.
    """
    html = textwrap.dedent(f"""\
    <div class="animate-fade-in" style="display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap;">
        <div class="glass-card" style="flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #00d2ff;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">📊</div>
            <div style="font-size: 1rem; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1px;">Total Records</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: white;">{total}</div>
        </div>
        <div class="glass-card" style="flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #28a745;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">✅</div>
            <div style="font-size: 1rem; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1px;">Valid KTP</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: #2ecc71;">{valid}</div>
        </div>
        <div class="glass-card" style="flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #dc3545;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">⚠️</div>
            <div style="font-size: 1rem; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1px;">Invalid KTP</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: #ff4757;">{invalid}</div>
        </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)

def render_flowchart_info():
    """
    Menampilkan alur diagram (flowchart) aplikasi menggunakan HTML/CSS.
    Menunjukkan proses dari upload gambar hingga masuk database.
    """
    html = textwrap.dedent("""\
    <div class="glass-card animate-fade-in" style="margin-top: 30px;">
        <h3 style="text-align: center; margin-bottom: 25px; color: white;">Alur Proses Sistem KTP OCR</h3>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 15px;">
            <div style="width: 80%; max-width: 400px; background: rgba(40, 167, 69, 0.2); border: 1px solid #28a745; padding: 15px; border-radius: 10px; text-align: center;">
                <strong style="color: white;">1. User Mengunggah Gambar KTP</strong><br>
                <small style="color: #b0b0b0;">(Format: JPG, PNG, JPEG)</small>
            </div>
            <div style="color: #00d2ff;">⬇️</div>
            <div style="width: 80%; max-width: 400px; background: rgba(155, 89, 182, 0.2); border: 1px solid #9b59b6; padding: 15px; border-radius: 10px; text-align: center;">
                <strong style="color: white;">2. Model Klasifikasi AI</strong><br>
                <small style="color: #b0b0b0;">(Mengecek apakah gambar adalah KTP Valid)</small>
            </div>
            <div style="color: #00d2ff;">⬇️</div>
            <div style="width: 80%; max-width: 400px; background: rgba(155, 89, 182, 0.2); border: 1px solid #9b59b6; padding: 15px; border-radius: 10px; text-align: center;">
                <strong style="color: white;">3. Ekstraksi Teks (OCR)</strong><br>
                <small style="color: #b0b0b0;">(Membaca NIK, Nama, Tanggal Lahir, dll menggunakan model OCR)</small>
            </div>
            <div style="color: #00d2ff;">⬇️</div>
            <div style="width: 80%; max-width: 400px; background: rgba(241, 196, 15, 0.2); border: 1px solid #f1c40f; padding: 15px; border-radius: 10px; text-align: center;">
                <strong style="color: white;">4. Parsing JSON</strong><br>
                <small style="color: #b0b0b0;">(Data terstruktur dalam format JSON)</small>
            </div>
            <div style="color: #00d2ff;">⬇️</div>
            <div style="width: 80%; max-width: 400px; background: rgba(52, 152, 219, 0.2); border: 1px solid #3498db; padding: 15px; border-radius: 10px; text-align: center;">
                <strong style="color: white;">5. Validasi Logika Bisnis</strong><br>
                <small style="color: #b0b0b0;">(Mengecek format NIK, kelogisan tanggal lahir, provinsi, dll)</small>
            </div>
            <div style="color: #00d2ff;">⬇️</div>
            <div style="width: 80%; max-width: 400px; background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; padding: 15px; border-radius: 10px; text-align: center;">
                <strong style="color: white;">6. Simpan ke Database</strong><br>
                <small style="color: #b0b0b0;">(Menyimpan hasil akhir untuk riwayat/reporting)</small>
            </div>
        </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)
