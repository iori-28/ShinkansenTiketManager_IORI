from fitur1 import jadwal
from fitur2 import pemesanan
from fitur3 import filter
from fitur4 import penumpang
from fitur5 import laporan
from fitur6 import refund

ADMIN_PASSWORD = "8948!"

def admin_menu():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Manajemen Jadwal")
        print("2. Laporan Penjualan")
        print("3. Manajemen Penumpang")
        print("4. History Refund")
        print("0. Kembali ke Halaman Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            jadwal.jadwal_admin()
        elif pilihan == '2':
            laporan.laporan_admin()
        elif pilihan == '3':
            penumpang.penumpang_admin()
        elif pilihan == '4':
            refund.refund_admin()
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

def user_menu():
    while True:
        print("\n=== MENU USER ===")
        print("1. Lihat Jadwal")
        print("2. Pencarian & Filter Jadwal")
        print("3. Pesan Tiket")
        print("4. Pembatalan Tiket")
        print("0. Kembali ke Halaman Utama")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            jadwal.jadwal_user()
        elif pilihan == '2':
            filter.filter_user()
        elif pilihan == '3':
            pemesanan.pemesanan_user()
        elif pilihan == '4':
            refund.refund_user()
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

def login_menu():
    while True:
        print("\n==== SHINKs APP ====")
        print("1. Masuk sebagai Admin")
        print("2. Masuk sebagai Consumer")
        print("0. Keluar")
        pilihan = input("Pilih: ")

        if pilihan == '1':
            pwd = input("Masukkan password admin: ")
            if pwd == ADMIN_PASSWORD:
                print("Login Admin berhasil!\n")
                admin_menu()
            else:
                print("Password salah! Akses ditolak.")
        elif pilihan == '2':
            print("Login User berhasil!\n")
            user_menu()
        elif pilihan == '0':
            print("Terima kasih sudah menggunakan SHINKs APP!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
