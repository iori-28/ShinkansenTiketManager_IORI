from fitur1 import jadwal
from fitur2 import pemesanan
from fitur3 import konfirmasi
from fitur4 import penumpang
from fitur5 import laporan
from fitur6 import refund
from utils import akun_user

ADMIN_PASSWORD = "8948!"

# fungsi buat jadi admin
def admin_menu():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Manajemen Jadwal")
        print("2. Manajemen Penumpang")
        print("3. Konfirmasi Tiket")
        print("4. History Refund")
        print("5. Laporan Penjualan")
        print("0. Kembali ke Halaman Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            jadwal.jadwal_admin()
        elif pilihan == '2':
            penumpang.penumpang_admin()
        elif pilihan == '3':
            konfirmasi.konfirmasi_tiket()
        elif pilihan == '4':
            refund.refund_admin()
        elif pilihan == '5':
            laporan.laporan_admin()
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

# fungsi buat jadi user
def user_login_menu(username):
    while True:
        print(f"\n=== MENU USER ({username}) ===")
        print("1. Lihat Jadwal")
        print("2. Pesan Tiket")
        print("3. Refund Tiket")
        print("4. Cek Saldo")
        print("5. Top-up Saldo")
        print("0. Kembali ke Halaman Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            jadwal.jadwal_user()
        elif pilihan == '2':
            pemesanan.pemesanan_user(username)
        elif pilihan == '3':
            refund.refund_user(username)
        elif pilihan == '4':
            akun_user.cek_saldo(username)
        elif pilihan == '5':
            akun_user.topup_saldo(username)
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

# fungsi user guest (tanpa login)
def user_guest_menu():
    while True:
        print("\n=== MENU TANPA AKUN ===")
        print("1. Lihat Jadwal")
        print("2. Pesan Tiket")
        print("3. Refund Tiket")
        print("0. Kembali ke Halaman Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            jadwal.jadwal_user()
        elif pilihan == '2':
            pemesanan.pemesanan_user("guest")  # tag username sebagai guest
        elif pilihan == '3':
            refund.refund_user("guest")
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

# ini yang pertama kali dijalankan
# menu awal login
def login_menu():
    while True:
        print("\n==== SHINKs APP ====")
        print("1. Masuk sebagai Admin")
        print("2. Masuk sebagai User")
        print("3. Lanjut tanpa Akun")
        print("4. Registrasi Akun Baru")
        print("0. Keluar Aplikasi")
        pilihan = input("Pilih: ")

        if pilihan == '1':
            pwd = input("Masukkan password admin: ")
            if pwd == ADMIN_PASSWORD:
                print("Login Admin berhasil!\n")
                admin_menu()
            else:
                print("Password salah! Akses ditolak.")
        elif pilihan == '2':
            username = akun_user.login_user()
            if username:
                user_login_menu(username)
        elif pilihan == '3':
            print("\n[!] Anda masuk sebagai pengguna tanpa akun.")
            user_guest_menu()
        elif pilihan == '4':
            akun_user.daftar_akun()
        elif pilihan == '0':
            print("Terima kasih sudah menggunakan SHINKs APP!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
