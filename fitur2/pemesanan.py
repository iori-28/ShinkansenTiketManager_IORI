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

    id_jadwal = input("Masukkan ID Jadwal yang dipilih: ").strip()
    if batal_input(id_jadwal): return
    dipilih = next((j for j in jadwal if j["id_jadwal"] == id_jadwal), None)
    if not dipilih:
        print("[!] Jadwal tidak ditemukan.")
        return

    jumlah_tiket = input("Jumlah tiket yang ingin dibeli: ")
    if batal_input(jumlah_tiket): return
    if not jumlah_tiket.isdigit() or int(jumlah_tiket) <= 0:
        print("[!] Jumlah tiket tidak valid.")
        return
    jumlah_tiket = int(jumlah_tiket)

    if jumlah_tiket > int(dipilih["kursi_tersedia"]):
        print("[!] Jumlah kursi tidak mencukupi.")
        return

    harga_total = jumlah_tiket * int(dipilih["harga"])

    if username and username != "guest":
        # === USER AKUN ===
        users = csv_handler.baca_csv("akun_user.csv")
        user = next((u for u in users if u["username"] == username), None)

        if not user:
            print("[!] Akun tidak ditemukan.")
            return

        if int(user["saldo"]) < harga_total:
            print(f"[!] Saldo tidak cukup. Total: ¥{harga_total}, Saldo Anda: ¥{user['saldo']}")
            return

        user["saldo"] = str(int(user["saldo"]) - harga_total)
        csv_handler.tulis_csv("akun_user.csv", users, users[0].keys())

        id_penumpang = username
        nama_penumpang = user["nama"]
        email_penumpang = user["email"]
        tipe_user = "akun"
    else:
        # === USER GUEST ===
        nama_penumpang = input("Masukkan nama penumpang: ").strip()
        if batal_input(nama_penumpang): return

        email_penumpang = input("Masukkan email penumpang: ").strip()
        if batal_input(email_penumpang): return

        id_penumpang = f"guest_{datetime.now().strftime('%H%M%S')}"
        tipe_user = "guest"

        # Simpan ke penumpang.csv
        data_penumpang = {
            "id_penumpang": id_penumpang,
            "nama_penumpang": nama_penumpang,
            "email_penumpang": email_penumpang,
            "user_SHINKs": "guest",
            "waktu_pesan": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        csv_handler.tambah_csv("penumpang.csv", data_penumpang, data_penumpang.keys())

    # Update kursi
    for j in jadwal:
        if j["id_jadwal"] == id_jadwal:
            j["kursi_tersedia"] = str(int(j["kursi_tersedia"]) - jumlah_tiket)
    csv_handler.tulis_csv("jadwal.csv", jadwal, jadwal[0].keys())

    # Simpan pemesanan
    data_pesan = {
        "id_pemesanan": str(uuid4())[:8],
        "id_penumpang": id_penumpang,
        "nama_penumpang": nama_penumpang,
        "email_penumpang": email_penumpang,
        "id_jadwal": id_jadwal,
        "jumlah_tiket": jumlah_tiket,
        "total_harga": harga_total,
        "status": "Berhasil",
        "waktu_pesan": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    if tipe_user == "akun":
        csv_handler.tambah_csv("pemesanan_akun.csv", data_pesan, data_pesan.keys())
    else:
        csv_handler.tambah_csv("pemesanan_guest.csv", data_pesan, data_pesan.keys())

    print(f"\n✅ Pemesanan berhasil!")
    print(f"Penumpang: {nama_penumpang}\nJumlah Tiket: {jumlah_tiket} | Total: ¥{harga_total}")
