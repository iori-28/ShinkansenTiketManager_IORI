# fitur6/refund.py
from utils import csv_handler
from datetime import datetime
from utils.helper import batal_input

def refund_user(username):
    print("\n=== AJUKAN PEMBATALAN TIKET ===")
    file = "pemesanan_akun.csv" if username != "guest" else "pemesanan_guest.csv"
    data = csv_handler.baca_csv(file)

    # Filter berdasarkan user
    data_user = [d for d in data if d["id_penumpang"] == username]

    if not data_user:
        print("[!] Tidak ada tiket yang bisa dibatalkan.")
        return

    # Tampilkan daftar pemesanan user
    for i, row in enumerate(data_user, 1):
        print(f"{i}. ID: {row['id_pemesanan']} | Jadwal: {row['id_jadwal']} | Total: ¥{row['total_harga']}")

    pilih = input("Masukkan nomor tiket yang ingin dibatalkan (0 untuk batal): ")
    if batal_input(pilih): return

    try:
        indeks = int(pilih) - 1
        dipilih = data_user[indeks]
    except:
        print("[!] Pilihan tidak valid.")
        return

    alasan = input("Alasan pembatalan: ").strip()
    if batal_input(alasan): return

    data_refund = {
        "id_refund": f"R{datetime.now().strftime('%H%M%S')}",
        "id_pemesanan": dipilih["id_pemesanan"],
        "nama_penumpang": dipilih.get("nama_penumpang", "-"),
        "email_penumpang": dipilih.get("email_penumpang", "-"),
        "alasan": alasan,
        "waktu_refund": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "jumlah_refund": dipilih["total_harga"]
    }

    csv_handler.tambah_csv("refund.csv", data_refund, data_refund.keys())
    print("\n[+] Pengajuan refund berhasil dikirim. Menunggu konfirmasi admin.")


# === BAGIAN UNTUK ADMIN ===
def refund_admin():
    print("\n=== KONFIRMASI REFUND OLEH ADMIN ===")
    data = csv_handler.baca_csv("refund.csv")

    if not data:
        print("[!] Tidak ada pengajuan refund.")
        return

    for i, row in enumerate(data, 1):
        print(f"{i}. ID Refund: {row['id_refund']} | Pemesan: {row.get('nama_penumpang','-')} | Email: {row.get('email_penumpang','-')} | Jumlah: ¥{row['jumlah_refund']} | Alasan: {row['alasan']}")

    pilih = input("Masukkan nomor refund yang akan dikonfirmasi (0 untuk batal): ")
    if batal_input(pilih): return

    try:
        idx = int(pilih) - 1
        refund = data[idx]
    except:
        print("[!] Pilihan tidak valid.")
        return

    id_pem = refund["id_pemesanan"]
    pemesanan_ditemukan = None
    sumber_file = None

    # Cari data pemesanan di file akun dan guest
    for file in ["pemesanan_akun.csv", "pemesanan_guest.csv"]:
        pemesanan = csv_handler.baca_csv(file)
        match = next((p for p in pemesanan if p["id_pemesanan"] == id_pem), None)
        if match:
            pemesanan_ditemukan = match
            sumber_file = file
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

    # Hapus refund dari daftar refund
    data = [r for r in data if r["id_refund"] != refund["id_refund"]]
    csv_handler.tulis_csv("refund.csv", data, data[0].keys() if data else refund.keys())

    print("\n[+] Refund berhasil dikonfirmasi dan dana dikembalikan.")
