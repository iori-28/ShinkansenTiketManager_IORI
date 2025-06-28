# menu jadwal for admin
def jadwal_admin():
    while True:
        print("\n=== MANAGEMEN JADWAL ===")
        print("1. Tambah Jadwal")
        print("2. Edit Jadwal")
        print("3. Hapus Jadwal")
        print("4. Lihat jadwal")
        print("0. Kembali ke Menu Admin")
        pilihan = input("Pilih Menu: ")
        if pilihan == '1':
            print("Fitur Tambah Jadwal belum tersedia.")
        elif pilihan == '2':
            print("Fitur Edit Jadwal belum tersedia.")
        elif pilihan == '3':
            print("Fitur Hapus Jadwal belum tersedia.")
        elif pilihan == '4':
            print("Fitur Lihat Jadwal belum tersedia.")
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

# def jadwal_user():
    