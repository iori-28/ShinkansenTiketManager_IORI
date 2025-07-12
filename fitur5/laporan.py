# fitur5/laporan.py
from utils import csv_handler
from datetime import datetime
from collections import defaultdict

def laporan_admin():
    print("\n=== LAPORAN PENJUALAN ===")

    data_konfirmasi = csv_handler.baca_csv("pemesanan_terkonfirmasi.csv")
    data_penumpang = csv_handler.baca_csv("penumpang.csv")

    if not data_konfirmasi:
        print("[!] Belum ada data pemesanan yang terkonfirmasi.")
        return

    # Ringkasan total dengan validasi
    try:
        total_tiket = sum(int(row["jumlah_tiket"]) for row in data_konfirmasi if row["jumlah_tiket"].isdigit())
        total_pendapatan = sum(int(row["total_harga"]) for row in data_konfirmasi if row["total_harga"].isdigit())
        total_pemesanan = len(data_konfirmasi)
        total_penumpang = len(set(row["id_penumpang"] for row in data_penumpang))
    except Exception as e:
        print("[!] Gagal menghitung ringkasan:", e)
        return

    print(f"\n📦 Total Tiket Terjual     : {total_tiket:,}")
    print(f"🧾 Total Pemesanan         : {total_pemesanan:,}")
    print(f"💰 Total Pendapatan        : ¥{total_pendapatan:,}")
    print(f"🧍 Total Penumpang Tercatat: {total_penumpang:,}")

    # Laporan harian
    laporan_harian = defaultdict(lambda: {"tiket": 0, "pendapatan": 0, "pemesanan": 0})

    for row in data_konfirmasi:
        waktu = row.get("waktu_konfirmasi", "")
        if not waktu: continue
        tanggal = waktu.split(" ")[0]

        try:
            laporan_harian[tanggal]["tiket"] += int(row["jumlah_tiket"])
            laporan_harian[tanggal]["pendapatan"] += int(row["total_harga"])
            laporan_harian[tanggal]["pemesanan"] += 1
        except:
            continue

    # Simpan ke laporan.csv
    laporan_csv = []
    for tanggal, nilai in sorted(laporan_harian.items()):
        laporan_csv.append({
            "tanggal": tanggal,
            "total_tiket_terjual": nilai["tiket"],
            "total_pemesanan": nilai["pemesanan"],
            "total_pendapatan": nilai["pendapatan"]
        })

    if laporan_csv:
        csv_handler.tulis_csv("laporan.csv", laporan_csv, laporan_csv[0].keys())

    # Tampilkan laporan harian
    print("\n📊 Ringkasan Laporan Harian:")
    for row in laporan_csv:
        print(f"{row['tanggal']} | Tiket: {row['total_tiket_terjual']:,} | "
              f"Pemesanan: {row['total_pemesanan']:,} | Pendapatan: ¥{row['total_pendapatan']:,}")

    # Hari dengan pendapatan tertinggi
    if laporan_csv:
        terbaik = max(laporan_csv, key=lambda x: x["total_pendapatan"])
        print(f"\n💹 Hari Pendapatan Tertinggi: {terbaik['tanggal']} (¥{terbaik['total_pendapatan']:,})")
