from utils import csv_handler

# Tampilkan semua penumpang yang pernah memesan tiket
def penumpang_admin():
    print("\n=== DATA PENUMPANG TERDAFTAR ===")

    data_penumpang = csv_handler.baca_csv("penumpang.csv")

    if not data_penumpang:
        print("[!] Belum ada data penumpang.")
        return

    print(f"Total Penumpang: {len(data_penumpang)}\n")
    for i, row in enumerate(data_penumpang, 1):
        print(f"{i}. ID: {row['id_penumpang']} | Nama: {row['nama_penumpang']} | "
              f"Email: {row['email_penumpang']} | Login: {row['user_SHINKs']}")