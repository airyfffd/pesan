# laporan_sensor_shift_full.py

import streamlit as st
from datetime import datetime, time, timedelta
import locale

# Mengatur locale ke Indonesia untuk format hari & bulan
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.utf8')
except:
    locale.setlocale(locale.LC_TIME, 'C')  # fallback kalau sistem tidak support

st.set_page_config(page_title="Laporan Harian Sensor", layout="centered")
st.title("📡 Laporan Harian Sensor Stageof Balikpapan")

# Input tanggal dan jam
tanggal_laporan = st.date_input("Tanggal Mulai Shift", value=datetime.today())
jam_mulai = st.time_input("Jam Mulai", value=time(7, 0))
jam_selesai = st.time_input("Jam Selesai", value=time(14, 30))

# Fungsi menentukan shift, ucapan dan format tanggal
def tentukan_shift_ucapan_tanggal(jam_mulai, jam_selesai, tanggal_awal):
    if jam_mulai == time(7, 0) and jam_selesai == time(14, 30):
        shift = "Pagi"
        ucapan = "Siang"
        hari_tanggal = tanggal_awal.strftime("%A, %d %B %Y")
    elif jam_mulai == time(13, 0) and jam_selesai == time(20, 30):
        shift = "Siang"
        ucapan = "Malam"
        hari_tanggal = tanggal_awal.strftime("%A, %d %B %Y")
    elif jam_mulai == time(20, 0) and jam_selesai == time(8, 30):
        shift = "Malam"
        ucapan = "Pagi"
        tanggal_akhir = tanggal_awal + timedelta(days=1)
        hari1 = tanggal_awal.strftime("%A")
        hari2 = tanggal_akhir.strftime("%A")
        tgl1 = tanggal_awal.day
        tgl2 = tanggal_akhir.day
        bulan = tanggal_awal.strftime("%B")
        tahun = tanggal_awal.year
        hari_tanggal = f"{hari1}–{hari2}, {tgl1}–{tgl2} {bulan} {tahun}"
    else:
        shift = "-"
        ucapan = "- (Jadwal tidak sesuai ketentuan)"
        hari_tanggal = "-"

    return shift, ucapan, hari_tanggal

shift, ucapan, hari_tanggal = tentukan_shift_ucapan_tanggal(jam_mulai, jam_selesai, tanggal_laporan)

# Pilihan kondisi sensor
opsi_sensor = st.radio("Status Sensor", ["ON SEMUA", "Ada yang OFF"])
sensor_off = ""
if opsi_sensor == "Ada yang OFF":
    sensor_off = st.text_input("Nama Sensor yang OFF (pisahkan dengan koma jika lebih dari satu)", placeholder="Contoh: MTKI, MTAK")

# Input petugas
st.subheader("Petugas On Duty")
jumlah_petugas = st.slider("Jumlah Petugas", 1, 5, 2)
petugas = []
for i in range(jumlah_petugas):
    nama = st.text_input(f"Nama Petugas #{i+1}", value="" if i >= 2 else ["U. Samosir", "Benny"][i])
    if nama:
        petugas.append(nama)

# Jumlah gempa
jumlah_gempa = st.number_input("Jumlah Gempa Tercatat", min_value=0, value=0)

# Tombol hasil
if st.button("📄 Buat Laporan"):
    st.markdown("### 📝 Hasil Laporan:")
    laporan = f"""
Selamat {ucapan}

Mohon izin melaporkan update kondisi sensor tanggung jawab Stageof Balikpapan.

Hari/Tanggal : {hari_tanggal}
Pukul: {jam_mulai.strftime('%H.%M')} - {jam_selesai.strftime('%H.%M')} WITA

Kondisi sensor {"ON SEMUA" if opsi_sensor == "ON SEMUA" else f"{sensor_off} OFF"}

On Duty {shift}
"""
    for idx, nama in enumerate(petugas, start=1):
        laporan += f"{idx}. {nama}\n"

    laporan += f"\nJumlah gempa di sekitar wilayah Kalimantan tercatat saat kami bertugas sebanyak {jumlah_gempa} kali"

    st.text(laporan)
