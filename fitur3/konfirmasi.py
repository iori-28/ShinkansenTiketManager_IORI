# konfirmasi.py
from utils import csv_handler
from utils.helper import batal_input
from datetime import datetime

def konfirmasi_tiket():
    print("\n=== KONFIRMASI TIKET OLEH ADMIN ===")

    # Gabungkan semua pemesanan dari user dan guest
    data_akun = csv_handler.baca_csv("pemesanan_akun.csv")
    data_guest = csv_handler.baca_csv("pemesanan_guest.csv")

    semua_pemesanan = []
    for row in data_akun:
        row["tipe"] = "akun"
        semua_pemesanan.append(row)
    for row in data_guest:
        row["tipe"] = "guest"
        semua_pemesanan.append(row)

    if not semua_pemesanan:
        print("[!] Tidak ada pemesanan yang menunggu konfirmasi.")
        return

    print("\nDaftar Pemesanan Belum Dikonfirmasi:")
    for i, row in enumerate(semua_pemesanan, 1):
        print(f"{i}. ID: {row['id_pemesanan']} | Penumpang: {row['id_penumpang']} | Jadwal: {row['id_jadwal']} | Tipe: {row['tipe']}")

    pilih = input("\nMasukkan nomor pemesanan yang ingin dikonfirmasi (pisahkan dengan koma), atau 0 untuk batal: ")
    if batal_input(pilih): return

    try:
        indeks_dipilih = [int(x.strip()) - 1 for x in pilih.split(",") if x.strip().isdigit() and int(x.strip()) > 0]
    except ValueError:
        print("[!] Input tidak valid.")
        return

    if not indeks_dipilih or any(i >= len(semua_pemesanan) for i in indeks_dipilih):
        print("[!] Tidak ada nomor yang valid.")
        return

    data_konfirmasi = []
    baru_data_akun = []
    baru_data_guest = []

    for i, row in enumerate(semua_pemesanan):
        if i in indeks_dipilih:
            row["status"] = "Terkonfirmasi"
            row["waktu_konfirmasi"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            data_konfirmasi.append(row)
        else:
            if row["tipe"] == "akun":
                baru_data_akun.append(row)
            else:
                baru_data_guest.append(row)

    # Tulis ulang file sumber
    csv_handler.tulis_csv("pemesanan_akun.csv", baru_data_akun, baru_data_akun[0].keys() if baru_data_akun else data_akun[0].keys())
    csv_handler.tulis_csv("pemesanan_guest.csv", baru_data_guest, baru_data_guest[0].keys() if baru_data_guest else data_guest[0].keys())

    # Tambahkan ke file terkonfirmasi
    csv_handler.tambah_csv("pemesanan_terkonfirmasi.csv", data_konfirmasi, data_konfirmasi[0].keys())

    print("\nTiket berhasil dikonfirmasi:")
    for row in data_konfirmasi:
        print(f"- {row['id_pemesanan']} ({row['tipe']})")
