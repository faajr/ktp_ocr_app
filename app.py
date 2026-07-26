import os
import io
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

import database
import validation
import openrouter_client
import ui_components

# ------------------------------------------------------------------
# Konfigurasi awal
# ------------------------------------------------------------------

load_dotenv()  # membaca isi file .env

API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "openrouter/free")

database.init_db()  # pastikan tabel database sudah ada

st.set_page_config(
    page_title="KTP OCR Intelligence",
    page_icon="🪪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject semua custom CSS (dark theme, glassmorphism, animasi, dll)
ui_components.inject_custom_css()


# ------------------------------------------------------------------
# Sidebar — navigasi & info
# ------------------------------------------------------------------

with st.sidebar:
    # Logo / judul sidebar
    st.markdown(
        """
        <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🪪</div>
            <div style="font-size: 1.1rem; font-weight: 700; letter-spacing: 0.5px;
                        background: linear-gradient(90deg, #00d2ff, #7b2ff7);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                KTP OCR Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Menu navigasi
    halaman = st.radio(
        "Menu",
        ["🏠 Home", "📤 Upload & Proses", "🗂️ Riwayat Database"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Info model AI
    st.markdown(
        f"""
        <div style="padding: 0.8rem; background: rgba(255,255,255,0.05);
                    border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 0.7rem; color: #888; text-transform: uppercase;
                        letter-spacing: 1px; margin-bottom: 0.4rem;">Model AI Aktif</div>
            <div style="font-size: 0.85rem; color: #00d2ff; font-weight: 500;">
                {MODEL_NAME}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not API_KEY:
        st.markdown(
            """
            <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(255,59,48,0.15);
                        border-radius: 10px; border: 1px solid rgba(255,59,48,0.3);
                        color: #ff6b6b; font-size: 0.85rem;">
                ⚠️ API key OpenRouter belum diisi di file <code>.env</code>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------------
# Halaman: HOME
# ------------------------------------------------------------------

if halaman == "🏠 Home":
    # Hero section
    ui_components.render_hero_section()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Flowchart info
    ui_components.render_flowchart_info()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Business rules yang digunakan
    st.markdown(
        """
        <div class="glass-card animate-fade-in" style="animation-delay: 0.4s;">
            <h3 style="color: #fff; margin-bottom: 1rem;">
                📋 Business Rules yang Digunakan
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.8rem;">
                <div style="padding: 0.8rem; background: rgba(0,210,255,0.08); border-radius: 10px;
                            border-left: 3px solid #00d2ff;">
                    <span style="color: #00d2ff;">①</span>
                    <span style="color: #ccc;"> Panjang NIK harus 16 digit</span>
                </div>
                <div style="padding: 0.8rem; background: rgba(0,210,255,0.08); border-radius: 10px;
                            border-left: 3px solid #00d2ff;">
                    <span style="color: #00d2ff;">②</span>
                    <span style="color: #ccc;"> NIK hanya boleh berisi angka</span>
                </div>
                <div style="padding: 0.8rem; background: rgba(123,47,247,0.1); border-radius: 10px;
                            border-left: 3px solid #7b2ff7;">
                    <span style="color: #7b2ff7;">③</span>
                    <span style="color: #ccc;"> Tanggal lahir dari NIK harus valid</span>
                </div>
                <div style="padding: 0.8rem; background: rgba(123,47,247,0.1); border-radius: 10px;
                            border-left: 3px solid #7b2ff7;">
                    <span style="color: #7b2ff7;">④</span>
                    <span style="color: #ccc;"> Jenis kelamin sesuai digit NIK</span>
                </div>
                <div style="padding: 0.8rem; background: rgba(52,199,89,0.1); border-radius: 10px;
                            border-left: 3px solid #34c759;">
                    <span style="color: #34c759;">⑤</span>
                    <span style="color: #ccc;"> Tanggal lahir di KTP cocok dengan NIK</span>
                </div>
                <div style="padding: 0.8rem; background: rgba(52,199,89,0.1); border-radius: 10px;
                            border-left: 3px solid #34c759;">
                    <span style="color: #34c759;">⑥</span>
                    <span style="color: #ccc;"> Masa berlaku masih aktif / SEUMUR HIDUP</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# Halaman: UPLOAD & PROSES
# ------------------------------------------------------------------

elif halaman == "📤 Upload & Proses":
    st.markdown(
        """
        <div class="animate-fade-in">
            <h1 style="color: #fff; font-size: 1.8rem; margin-bottom: 0.3rem;">
                📤 Upload & Proses Dokumen
            </h1>
            <p style="color: #888; font-size: 0.95rem; margin-bottom: 1.5rem;">
                Unggah gambar KTP untuk diproses oleh AI — klasifikasi, OCR, dan validasi otomatis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload gambar KTP",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        help="Format yang didukung: JPG, JPEG, PNG",
    )

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()

        # Layout 2 kolom: gambar + hasil
        col_gambar, col_hasil = st.columns([1, 2], gap="large")

        with col_gambar:
            st.markdown(
                """
                <div class="glass-card animate-fade-in" style="padding: 0.8rem;">
                    <div style="font-size: 0.75rem; color: #888; text-transform: uppercase;
                                letter-spacing: 1px; margin-bottom: 0.5rem;">
                        📷 Preview Dokumen
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.image(image_bytes, use_container_width=True)

        with col_hasil:
            if not API_KEY:
                st.markdown(
                    """
                    <div class="glass-card" style="border-color: rgba(255,59,48,0.4);">
                        <div style="color: #ff6b6b; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
                            ⚠️ API Key Tidak Ditemukan
                        </div>
                        <p style="color: #aaa;">
                            Isi dulu <code>OPENROUTER_API_KEY</code> di file <code>.env</code> kamu.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                tombol_proses = st.button(
                    "🚀 Proses Dokumen", type="primary", use_container_width=True
                )

                if tombol_proses:
                    # ========== STEP 1: Upload (sudah selesai) ==========
                    ui_components.render_step_progress(1)

                    # ========== STEP 2: Klasifikasi AI ==========
                    with st.spinner("🤖 Mengklasifikasi gambar..."):
                        hasil_klasifikasi = openrouter_client.classify_image(
                            image_bytes, API_KEY, MODEL_NAME
                        )

                    ui_components.render_step_progress(2)

                    if hasil_klasifikasi["is_ktp"]:
                        html_klasifikasi = """
<div class="glass-card animate-fade-in">
    <h3 style="color: #fff; margin-bottom: 0.8rem;">🤖 Step 2 — Klasifikasi AI</h3>
    <div style="padding: 1rem; background: rgba(52,199,89,0.15); border-radius: 12px; border: 1px solid rgba(52,199,89,0.3);">
        <span style="font-size: 1.5rem;">✅</span>
        <span style="color: #34c759; font-size: 1.1rem; font-weight: 600; margin-left: 0.5rem;">Dokumen Terdeteksi: KTP Indonesia</span>
        <p style="color: #8fbc8f; margin: 0.5rem 0 0 2.5rem; font-size: 0.9rem;">Gambar diklasifikasikan sebagai dokumen KTP. Melanjutkan ke tahap OCR...</p>
    </div>
</div>
"""
                        st.markdown(html_klasifikasi, unsafe_allow_html=True)
                    else:
                        html_klasifikasi = """
<div class="glass-card animate-fade-in">
    <h3 style="color: #fff; margin-bottom: 0.8rem;">🤖 Step 2 — Klasifikasi AI</h3>
    <div style="padding: 1rem; background: rgba(255,59,48,0.15); border-radius: 12px; border: 1px solid rgba(255,59,48,0.3);">
        <span style="font-size: 1.5rem;">❌</span>
        <span style="color: #ff6b6b; font-size: 1.1rem; font-weight: 600; margin-left: 0.5rem;">Bukan Dokumen KTP</span>
        <p style="color: #cc8888; margin: 0.5rem 0 0 2.5rem; font-size: 0.9rem;">Gambar bukan KTP Indonesia. Proses dihentikan.</p>
    </div>
</div>
"""
                        st.markdown(html_klasifikasi, unsafe_allow_html=True)
                        st.stop()

                    # ========== STEP 3 & 4: OCR Extraction + JSON Result ==========
                    with st.spinner("📝 Membaca isi KTP (OCR)..."):
                        hasil_ocr = openrouter_client.extract_ocr(
                            image_bytes, API_KEY, MODEL_NAME
                        )

                    ui_components.render_step_progress(4)

                    html_ocr = """
<div class="glass-card animate-fade-in" style="animation-delay: 0.2s;">
    <h3 style="color: #fff; margin-bottom: 0.8rem;">📝 Step 3–4 — Hasil OCR (JSON)</h3>
"""
                    if "error" in hasil_ocr:
                        html_ocr += f"""
<div style="padding: 1rem; background: rgba(255,59,48,0.15); border-radius: 12px; border: 1px solid rgba(255,59,48,0.3); color: #ff6b6b;">
    ⚠️ {hasil_ocr['error']}
</div>
</div>
"""
                        st.markdown(html_ocr, unsafe_allow_html=True)
                        st.stop()
                    else:
                        html_ocr += ui_components.get_ocr_result_cards_html(hasil_ocr)
                        html_ocr += "</div>"
                        st.markdown(html_ocr, unsafe_allow_html=True)

                    # ========== STEP 5: Validasi ==========
                    hasil_validasi = validation.validate_ktp(hasil_ocr)

                    ui_components.render_step_progress(5)

                    html_validasi = """
<div class="glass-card animate-fade-in" style="animation-delay: 0.4s;">
"""
                    
                    status = hasil_validasi["status_keseluruhan"]
                    
                    if status == "VALID":
                        html_validasi += """
<h3 style="color: #fff; margin-bottom: 0.8rem;">✅ Step 5 — Validasi Business Rule</h3>
<div style="padding: 0.8rem 1rem; background: rgba(52,199,89,0.15); border-radius: 10px; border: 1px solid rgba(52,199,89,0.3); color: #34c759; font-weight: 600; margin-bottom: 1rem;">
    Status Keseluruhan: VALID ✅
</div>
"""
                    else:
                        html_validasi += """
<h3 style="color: #fff; margin-bottom: 0.8rem;">❌ Step 5 — Validasi Business Rule</h3>
<div style="padding: 0.8rem 1rem; background: rgba(255,59,48,0.15); border-radius: 10px; border: 1px solid rgba(255,59,48,0.3); color: #ff6b6b; font-weight: 600; margin-bottom: 1rem;">
    Status Keseluruhan: INVALID ❌
</div>
"""
                        
                    html_validasi += ui_components.get_validation_table_html(hasil_validasi["detail"])
                    html_validasi += "</div>"
                    st.markdown(html_validasi, unsafe_allow_html=True)

                    # ========== STEP 6: Simpan ke Database ==========
                    ui_components.render_step_progress(6)

                    html_simpan = '<div class="glass-card animate-fade-in" style="animation-delay: 0.6s;">'
                    if status == "VALID":
                        database.save_record(
                            ocr_data=hasil_ocr,
                            status_validasi=status,
                            detail_validasi=hasil_validasi["detail"],
                        )
                        html_simpan += """
<h3 style="color: #fff; margin-bottom: 0.8rem;">💾 Step 6A — Simpan ke Database</h3>
<div style="padding: 1rem; background: rgba(52,199,89,0.15); border-radius: 12px; border: 1px solid rgba(52,199,89,0.3);">
    <span style="font-size: 1.5rem;">✅</span>
    <span style="color: #34c759; font-size: 1.05rem; font-weight: 600; margin-left: 0.5rem;">Data Berhasil Disimpan!</span>
    <p style="color: #8fbc8f; margin: 0.5rem 0 0 2.5rem; font-size: 0.9rem;">Hasil OCR yang valid telah disimpan ke database. Lihat di menu <strong>🗂️ Riwayat Database</strong>.</p>
</div>
"""
                    else:
                        database.save_record(
                            ocr_data=hasil_ocr,
                            status_validasi=status,
                            detail_validasi=hasil_validasi["detail"],
                        )
                        html_simpan += """
<h3 style="color: #fff; margin-bottom: 0.8rem;">⚠️ Step 6B — Data Tidak Valid</h3>
<div style="padding: 1rem; background: rgba(255,149,0,0.15); border-radius: 12px; border: 1px solid rgba(255,149,0,0.3);">
    <span style="font-size: 1.5rem;">⚠️</span>
    <span style="color: #ff9500; font-size: 1.05rem; font-weight: 600; margin-left: 0.5rem;">Data Tersimpan dengan Status INVALID</span>
    <p style="color: #ccaa66; margin: 0.5rem 0 0 2.5rem; font-size: 0.9rem;">Beberapa field tidak lolos validasi business rule. Data tetap disimpan untuk review di menu <strong>🗂️ Riwayat Database</strong>.</p>
</div>
"""
                    html_simpan += "</div>"
                    st.markdown(html_simpan, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Halaman: RIWAYAT DATABASE
# ------------------------------------------------------------------

elif halaman == "🗂️ Riwayat Database":
    st.markdown(
        """
        <div class="animate-fade-in">
            <h1 style="color: #fff; font-size: 1.8rem; margin-bottom: 0.3rem;">
                🗂️ Riwayat Database
            </h1>
            <p style="color: #888; font-size: 0.95rem; margin-bottom: 1.5rem;">
                Semua hasil OCR yang pernah diproses, beserta status validasinya.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Statistik ringkasan
    stats = database.get_statistics()
    ui_components.render_stat_cards(stats["total"], stats["valid"], stats["invalid"])

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Ambil semua data
    data = database.get_all_records()

    if not data:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <div style="color: #888; font-size: 1.1rem;">
                    Belum ada data yang tersimpan.
                </div>
                <div style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">
                    Silakan upload dokumen di menu <strong>📤 Upload & Proses</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Tabel data
        st.markdown(
            """
            <div class="glass-card animate-fade-in" style="margin-bottom: 1rem;">
                <h3 style="color: #fff; margin-bottom: 0;">📊 Data Tersimpan</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Siapkan dataframe untuk ditampilkan
        df = pd.DataFrame(data)
        df_tampil = df[
            ["id", "nama", "nomor_dokumen", "jenis_dokumen", "tanggal_upload", "status_validasi"]
        ].copy()
        df_tampil.columns = ["ID", "Nama", "NIK", "Jenis", "Tanggal Upload", "Status"]

        st.dataframe(
            df_tampil,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            },
        )

        # Hapus st.markdown("</div>") di sini karena glass-card sudah ditutup di header.

        # Detail view — pilih record untuk lihat detail
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="glass-card animate-fade-in" style="animation-delay: 0.2s; margin-bottom: 1rem;">
                <h3 style="color: #fff; margin-bottom: 0;">🔍 Detail Record</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Selectbox untuk memilih record
        pilihan_id = st.selectbox(
            "Pilih ID record untuk melihat detail:",
            options=[d["id"] for d in data],
            format_func=lambda x: f"ID {x} — {next((d['nama'] for d in data if d['id'] == x), '?')}",
        )

        if pilihan_id:
            record = database.get_record_by_id(pilihan_id)
            if record:
                col_ocr, col_val = st.columns(2, gap="medium")

                with col_ocr:
                    st.markdown(
                        """<div style="font-size: 0.8rem; color: #888; text-transform: uppercase;
                                      letter-spacing: 1px; margin-bottom: 0.5rem;">
                            📝 Data OCR
                        </div>""",
                        unsafe_allow_html=True,
                    )
                    try:
                        ocr_json = json.loads(record["data_ocr_json"])
                        st.markdown(ui_components.get_ocr_result_cards_html(ocr_json), unsafe_allow_html=True)
                    except (json.JSONDecodeError, TypeError):
                        st.info("Data OCR tidak tersedia.")

                with col_val:
                    st.markdown(
                        """<div style="font-size: 0.8rem; color: #888; text-transform: uppercase;
                                      letter-spacing: 1px; margin-bottom: 0.5rem;">
                            ✅ Detail Validasi
                        </div>""",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"<div style='margin-bottom: 0.5rem;'>"
                        f"{ui_components.render_status_badge(record['status_validasi'])}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    try:
                        val_json = json.loads(record["detail_validasi_json"])
                        st.markdown(ui_components.get_validation_table_html(val_json), unsafe_allow_html=True)
                    except (json.JSONDecodeError, TypeError):
                        st.info("Detail validasi tidak tersedia.")
""""                      
            # Tambahkan tombol Hapus Data
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            col_spacer, col_hapus = st.columns([3, 1])
            with col_hapus:
                if st.button("🗑️ Hapus Data Ini", type="secondary", use_container_width=True):
                    database.delete_record(pilihan_id)
                    st.success("Data berhasil dihapus!")
                    st.rerun()
""""
        # Tombol export CSV
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        buffer_csv = io.StringIO()
        df_tampil.to_csv(buffer_csv, index=False)
        st.download_button(
            label="⬇️ Export ke CSV",
            data=buffer_csv.getvalue(),
            file_name="riwayat_ktp.csv",
            mime="text/csv",
            use_container_width=True,
        )
