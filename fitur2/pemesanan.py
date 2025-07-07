from utils import csv_handler
from datetime import datetime
from uuid import uuid4
from fitur1.jadwal import tampilkan_jadwal, filter_jadwal
from utils.helper import batal_input


def pemesanan_user(username=None):
    print("\n=== PEMESANAN TIKET SHINKANSEN ===")
    jadwal = csv_handler.baca_csv("jadwal.csv")

    if not jadwal:
        print("[!] Tidak ada jadwal tersedia.")
        return

    tampilkan_jadwal(jadwal)
    hasil = filter_jadwal()
    if not hasil:
        return

    # Pilih jadwal
    id_jadwal = input("Masukkan ID Jadwal yang dipilih: ").strip()
    if batal_input(id_jadwal): return
    dipilih = next((j for j in jadwal if j["id_jadwal"] == id_jadwal), None)
    if not dipilih:
        print("[!] Jadwal tidak ditemukan.")
        return

    # Input jumlah tiket
    jumlah_tiket = input("Jumlah tiket yang ingin dibeli: ")
    if batal_input(jumlah_tiket): return
    if not jumlah_tiket.isdigit() or int(jumlah_tiket) <= 0:
        print("[!] Jumlah tiket tidak valid.")
        return
    jumlah_tiket = int(jumlah_tiket)

    if jumlah_tiket > int(dipilih["kursi_tersedia"]):
        print("[!] Jumlah kursi tidak mencukupi.")
        return

    total_harga = jumlah_tiket * int(dipilih["harga"])
    waktu_pesan = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Penanganan untuk akun login
    if username and username != "guest":
        akun_list = csv_handler.baca_csv("akun_user.csv")
        user = next((u for u in akun_list if u["username"] == username), None)
        if not user:
            print("[!] Akun tidak ditemukan.")
            return

        if int(user["saldo"]) < total_harga:
            print(f"[!] Saldo tidak cukup. Total: ¥{total_harga}, Saldo Anda: ¥{user['saldo']}")
            return

        # Potong saldo
        user["saldo"] = str(int(user["saldo"]) - total_harga)
        csv_handler.tulis_csv("akun_user.csv", akun_list, akun_list[0].keys())

        nama_penumpang = user["nama"]
        id_penumpang = username
        target_file = "pemesanan_akun.csv"
    else:
        # Guest user
        nama_penumpang = input("Masukkan nama penumpang: ").strip()
        if batal_input(nama_penumpang): return
        id_penumpang = f"guest_{datetime.now().strftime('%H%M%S')}"
        target_file = "pemesanan_guest.csv"

    # Update kursi
    for j in jadwal:
        if j["id_jadwal"] == id_jadwal:
            j["kursi_tersedia"] = str(int(j["kursi_tersedia"]) - jumlah_tiket)
    csv_handler.tulis_csv("jadwal.csv", jadwal, jadwal[0].keys())

    # Data pemesanan
    data_pesan = {
        "id_pemesanan": str(uuid4())[:8],
        "id_penumpang": id_penumpang,
        "id_jadwal": id_jadwal,
        "jumlah_tiket": jumlah_tiket,
        "total_harga": total_harga,
        "status": "Berhasil",
        "waktu_pesan": waktu_pesan
    }

    # Tambahkan kolom username jika akun login
    if username and username != "guest":
        data_pesan["username"] = username

    csv_handler.tambah_csv(target_file, data_pesan, data_pesan.keys())

    print(f"\n✅ Pemesanan berhasil!")
    print(f"Penumpang: {nama_penumpang}")
    print(f"Jumlah Tiket: {jumlah_tiket}")
    print(f"Total Harga: ¥{total_harga}")
