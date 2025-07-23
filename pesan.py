import streamlit as st
from datetime import datetime, timedelta
import pyperclip

# Fungsi translate
def translate_day(day_en):
    hari = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis",
        "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    return hari.get(day_en, day_en)

def translate_month(month_en):
    bulan = {
        "January": "Januari", "February": "Februari", "March": "Maret", "April": "April",
        "May": "Mei", "June": "Juni", "July": "Juli", "August": "Agustus",
        "September": "September", "October": "Oktober", "November": "November", "December": "Desember"
    }
    return bulan.get(month_en, month_en)

# Konfigurasi halaman
st.set_page_config(page_title="Laporan Sensor", layout="centered")
st.title("📡 Laporan Harian Sensor Stageof Balikpapan")

# Input tanggal
tanggal_shift = st.date_input("Tanggal Shift", value=datetime.today())

# Data shift tetap
shift_opsi = {
    "Pagi (07.00 - 14.30 WITA)": {
        "shift": "Pagi",
        "ucapan": "Siang",
        "jam": "07.00 - 14.30 WITA",
        "tanggal_format": lambda d: f"{translate_day(d.strftime('%A'))}, {d.day} {translate_month(d.strftime('%B'))} {d.year}"
    },
    "Siang (13.00 - 20.30 WITA)": {
        "shift": "Siang",
        "ucapan": "Malam",
        "jam": "13.00 - 20.30 WITA",
        "tanggal_format": lambda d: f"{translate_day(d.strftime('%A'))}, {d.day} {translate_month(d.strftime('%B'))} {d.year}"
    },
    "Malam (20.00 - 08.30 WITA)": {
        "shift": "Malam",
        "ucapan": "Pagi",
        "jam": "20.00 - 08.30 WITA",
        "tanggal_format": lambda d: (
            f"{translate_day(d.strftime('%A'))}–{translate_day((d + timedelta(days=1)).strftime('%A'))}, "
            f"{d.day}–{(d + timedelta(days=1)).day} {translate_month(d.strftime('%B'))} {d.year}"
        )
    }
}

shift_pilihan = st.selectbox("Pilih Shift", list(shift_opsi.keys()))
data_shift = shift_opsi[shift_pilihan]

# Sensor status
opsi_sensor = st.radio("Status Sensor", ["ON SEMUA", "Ada yang OFF"])
sensor_off = ""
if opsi_sensor == "Ada yang OFF":
    sensor_off = st.text_input("Nama Sensor yang OFF", placeholder="Contoh: MTKI, MTAK")

# Petugas
st.subheader("Petugas On Duty")
jumlah_petugas = st.slider("Jumlah Petugas", 1, 5, 2)
petugas = []
for i in range(jumlah_petugas):
    nama = st.text_input(f"Nama Petugas #{i+1}", value="" if i >= 2 else ["U. Samosir", "Benny"][i])
    if nama:
        petugas.append(nama)

# Jumlah gempa
jumlah_gempa = st.number_input("Jumlah Gempa Tercatat", min_value=0, value=0)

# Generate laporan
if st.button("📄 Buat Laporan"):
    hari_tanggal = data_shift["tanggal_format"](tanggal_shift)
    laporan = f"""Selamat {data_shift['ucapan']}

Mohon izin melaporkan update kondisi sensor tanggung jawab Stageof Balikpapan.

Hari/Tanggal : {hari_tanggal}
Pukul: {data_shift['jam']}

Kondisi sensor {"ON SEMUA" if opsi_sensor == "ON SEMUA" else f"{sensor_off} OFF"}

On Duty {data_shift['shift']}"""
    for idx, nama in enumerate(petugas, start=1):
        laporan += f"\n{idx}. {nama}"

    laporan += f"\n\nJumlah gempa di sekitar wilayah Kalimantan tercatat saat kami bertugas sebanyak {jumlah_gempa} kali"

    st.markdown("### 📝 Hasil Laporan:")
    text_area = st.text_area("Laporan", laporan, height=300, key="laporan_textarea")

    # Tombol salin dengan fallback
    if st.button("📋 Salin ke Clipboard"):
        try:
            pyperclip.copy(laporan)
            st.success("✅ Laporan berhasil disalin ke clipboard!")
        except Exception as e:
            st.error(f"❌ Gagal menyalin otomatis. Silakan salin manual dari text area di atas.")
            st.markdown("""
            **Cara menyalin manual:**
            1. Klik pada text area di atas
            2. Tekan Ctrl+A (untuk memilih semua)
            3. Tekan Ctrl+C (untuk menyalin)
            4. Tekan Enter untuk keluar dari mode seleksi
            """)

    # Alternatif textarea yang auto-select
    st.markdown("""
    <style>
    .auto-select {
        width: 100%;
        height: 300px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    </style>
    <textarea class="auto-select" onclick="this.select()" readonly>{laporan}</textarea>
    """, unsafe_allow_html=True)
