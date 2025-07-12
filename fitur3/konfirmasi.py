# konfirmasi.py
from utils import csv_handler
from utils.helper import batal_input
from utils.fieldnames import fieldnames_pemesanan
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
        print(f"{i}. ID: {row['id_pemesanan']} | Penumpang: {row['id_penumpang']} | "
              f"Nama Penumpang: {row['nama_penumpang']} | Jadwal: {row['id_jadwal']} | Tipe: {row['tipe']}")

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

    # Simpan ulang file sumber
    csv_handler.tulis_csv("pemesanan_akun.csv", baru_data_akun, fieldnames_pemesanan)
    csv_handler.tulis_csv("pemesanan_guest.csv", baru_data_guest, fieldnames_pemesanan)
    csv_handler.tambah_csv("pemesanan_terkonfirmasi.csv", data_konfirmasi, fieldnames_pemesanan)

    # Tambahkan penumpang yang belum tercatat
    data_penumpang = csv_handler.baca_csv("penumpang.csv")
    id_tercatat = {p["id_penumpang"] for p in data_penumpang}

    for row in data_konfirmasi:
        if row["id_penumpang"] not in id_tercatat:
            baris = {
                "id_penumpang": row["id_penumpang"],
                "nama_penumpang": row["nama_penumpang"],
                "email_penumpang": row.get("email_penumpang", "-"),
                "user_SHINKs": "True" if row["tipe"] == "akun" else "False"
            }
            csv_handler.tambah_csv("penumpang.csv", baris, baris.keys())


    print("\nTiket berhasil dikonfirmasi:")
    for row in data_konfirmasi:
        print(f"- {row['id_pemesanan']} ({row['tipe']})")

def konfirmasi_refund():
    print("\n=== KONFIRMASI REFUND OLEH ADMIN ===")
    data = csv_handler.baca_csv("refund.csv")

    if not data:
        print("[!] Tidak ada pengajuan refund.")
        return

    for i, row in enumerate(data, 1):
        print(f"{i}. ID Refund: {row['id_refund']} | Pemesan: {row.get('nama_penumpang','-')} | "
              f"Email: {row.get('email_penumpang','-')} | Jumlah: \u00a5{row['jumlah_refund']} | "
              f"Alasan: {row['alasan']}")

    pilih = input("Masukkan nomor refund yang akan dikonfirmasi (0 untuk batal): ")
    if batal_input(pilih): return

    try:
        idx = int(pilih) - 1
        refund = data[idx]
    except:
        print("[!] Pilihan tidak valid.")
        return

    id_pem = refund["id_pemesanan"]
    id_jadwal = refund["id_jadwal"]
    jumlah_tiket = int(refund["jumlah_tiket"])
    pemesanan_ditemukan = None

    # Kembalikan kursi ke jadwal
    jadwal = csv_handler.baca_csv("jadwal.csv")
    for j in jadwal:
        if j["id_jadwal"] == id_jadwal:
            j["kursi_tersedia"] = str(int(j["kursi_tersedia"]) + jumlah_tiket)
            break
    csv_handler.tulis_csv("jadwal.csv", jadwal, jadwal[0].keys())

    # Cari dan hapus pemesanan di file akun atau guest
    for file in ["pemesanan_akun.csv", "pemesanan_guest.csv"]:
        pemesanan = csv_handler.baca_csv(file)
        match = next((p for p in pemesanan if p["id_pemesanan"] == id_pem), None)
        if match:
            pemesanan_ditemukan = match
            pemesanan.remove(match)
            csv_handler.tulis_csv(file, pemesanan, pemesanan[0].keys() if pemesanan else match.keys())
            break

    if not pemesanan_ditemukan:
        print("[!] Data pemesanan tidak ditemukan.")
        return

    # Jika akun user, tambahkan saldo
    if not pemesanan_ditemukan["id_penumpang"].startswith("guest"):
        users = csv_handler.baca_csv("akun_user.csv")
        for user in users:
            if user["username"] == pemesanan_ditemukan["id_penumpang"]:
                user["saldo"] = str(int(user["saldo"]) + int(refund["jumlah_refund"]))
                csv_handler.tulis_csv("akun_user.csv", users, users[0].keys())
                break

    # Hapus dari refund.csv
    data = [r for r in data if r["id_refund"] != refund["id_refund"]]
    csv_handler.tulis_csv("refund.csv", data, data[0].keys() if data else refund.keys())

    print("\n[+] Refund berhasil dikonfirmasi, kursi dikembalikan, dan saldo dikembalikan jika perlu.")