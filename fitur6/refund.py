# fitur6/refund.py
from utils import csv_handler
from datetime import datetime
from utils.helper import batal_input

# === BAGIAN UNTUK USER / GUEST ===
def refund_user(username):
    print("\n=== AJUKAN PEMBATALAN TIKET ===")
    file = "pemesanan_akun.csv" if username != "guest" else "pemesanan_guest.csv"
    data = csv_handler.baca_csv(file)

    # Filter data berdasarkan username / guest
    data_user = [d for d in data if d["id_penumpang"] == username]

    if not data_user:
        print("[!] Tidak ada tiket yang bisa dibatalkan.")
        return

    for i, row in enumerate(data_user, 1):
        print(f"{i}. ID Pemesanan: {row['id_pemesanan']} | Jadwal: {row['id_jadwal']} | Total: ¥{row['total_harga']}")

    pilih = input("Masukkan ID Pemesanan yang ingin dibatalkan (0 untuk batal): ").strip()
    if batal_input(pilih): return

    dipilih = next((d for d in data_user if d["id_pemesanan"] == pilih), None)
    if not dipilih:
        print("[!] ID tidak ditemukan.")
        return

    alasan = input("Alasan pembatalan: ").strip()
    if batal_input(alasan): return

    data_refund = {
        "id_refund": f"R{datetime.now().strftime('%H%M%S')}",
        "id_pemesanan": dipilih["id_pemesanan"],
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
        print(f"{i}. ID Refund: {row['id_refund']} | ID Pemesanan: {row['id_pemesanan']} | Jumlah: ¥{row['jumlah_refund']} | Alasan: {row['alasan']}")

    pilih = input("Masukkan ID Refund yang akan dikonfirmasi (0 untuk batal): ").strip()
    if batal_input(pilih): return

    refund = next((r for r in data if r["id_refund"] == pilih), None)
    if not refund:
        print("[!] ID Refund tidak ditemukan.")
        return

    id_pem = refund["id_pemesanan"]

    # Cek apakah pemesanan dari user atau guest
    for sumber in ["pemesanan_akun.csv", "pemesanan_guest.csv"]:
        pemesanan = csv_handler.baca_csv(sumber)
        match = next((p for p in pemesanan if p["id_pemesanan"] == id_pem), None)
        if match:
            pemesanan.remove(match)
            csv_handler.tulis_csv(sumber, pemesanan, pemesanan[0].keys() if pemesanan else match.keys())
            break

    # Update saldo jika user
    if not match["id_penumpang"].startswith("guest"):
        users = csv_handler.baca_csv("akun_user.csv")
        for user in users:
            if user["username"] == match["id_penumpang"]:
                user["saldo"] = str(int(user["saldo"]) + int(refund["jumlah_refund"]))
                csv_handler.tulis_csv("akun_user.csv", users, users[0].keys())
                break

    # Hapus dari refund.csv setelah diproses
    data = [r for r in data if r["id_refund"] != pilih]
    csv_handler.tulis_csv("refund.csv", data, data[0].keys() if data else refund.keys())

    print("[+] Refund berhasil dikonfirmasi dan dana dikembalikan.")
