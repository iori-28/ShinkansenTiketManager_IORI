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
        print(f"{i}. ID: {row['id_pemesanan']} | Jadwal: {row['id_jadwal']} | Total: \u00a5{row['total_harga']}")

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
        "id_jadwal": dipilih["id_jadwal"],
        "jumlah_tiket": dipilih["jumlah_tiket"],
        "nama_penumpang": dipilih.get("nama_penumpang", "-"),
        "email_penumpang": dipilih.get("email_penumpang", "-"),
        "alasan": alasan,
        "waktu_refund": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "jumlah_refund": dipilih["total_harga"]
    }

    csv_handler.tambah_csv("refund.csv", data_refund, data_refund.keys())
    print("\n[+] Pengajuan refund berhasil dikirim. Menunggu konfirmasi admin.")