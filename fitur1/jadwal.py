from utils import csv_handler
from datetime import datetime
from utils.fieldnames import fieldnames_jadwal, fieldnames_terhapus
from utils.helper import batal_input


# fungsi managemen jadwal admin
def jadwal_admin():
    while True:
        print("\n=== MANAGEMEN JADWAL ===")
        print("1. Lihat jadwal")
        print("2. Update Jadwal")
        print("0. Kembali ke Menu Admin")
        pilihan = input("Pilih Menu: ")
        if pilihan == '1':
            lihat_jadwal()
        elif pilihan == '2':
            update_jadwal()
        elif pilihan == '0':
            break
        else:
            print("Pilihan tidak valid!")

# menu update jadwal
def update_jadwal():
    while True:
        print("\n=== UPDATE JADWAL ===")
        print("1. Tambah Jadwal")
        print("2. Hapus Jadwal")
        print("3. Pulihkan Jadwal")
        print("4. Update Kursi")
        print("0. Kembali")
        pilih = input("Pilih menu edit: ")

        if pilih == '1':
            lihat_jadwal()
            tambah_jadwal()
        elif pilih == '2':
            lihat_jadwal()
            hapus_jadwal()
        elif pilih == '3':
            restore_jadwal()
        elif pilih == '4':
            update_kursi_jadwal()
        elif pilih == '0':
            break
        else:
            print("Pilihan tidak valid!")

# menu tambah jadwal
def tambah_jadwal():
    print("\n=== TAMBAH JADWAL ===")
    data = csv_handler.baca_csv("jadwal.csv")
    
    print("Ketik 0 kapan saja untuk membatalkan proses.")

    # validasi id_jadwal
    while True:
        id_baru = input("ID Jadwal (misal J001): ")
        if batal_input(id_baru): return
       
        id_sudah_ada = any(row["id_jadwal"] == id_baru for row in data)
        if id_sudah_ada:
            print(f"[!] ID {id_baru} sudah terdaftar. Coba masukkan ID lain.")
        else:
            break  # ngecek ID, kalo valid bakal keluar dari loop
    
    asal = input("Stasiun Asal: ")
    if batal_input(asal): return
    tujuan = input("Stasiun Tujuan: ")
    if batal_input(tujuan): return
    # banyak if batal_input() incase si admin gajadi tambah jadwal

    # validasi input waktu berangkat
    while True:
        waktu_berangkat_input = input("Waktu Berangkat (format: MM/DD/YYYY HH:MM): ")
        if batal_input(waktu_berangkat_input): return
        try:
            waktu_berangkat = datetime.strptime(waktu_berangkat_input, "%m/%d/%Y %H:%M")
            break  # Keluar loop kalau formatnya benar
        except ValueError:
            print("[!] Format waktu salah. Coba lagi, contoh: 06/30/2025 08:00")

    # validasi input waktu tiba
    while True:
        waktu_tiba_input = input("Waktu Tiba (format: MM/DD/YYYY HH:MM): ")
        if batal_input(waktu_tiba_input): return
        try:
            waktu_tiba = datetime.strptime(waktu_tiba_input, "%m/%d/%Y %H:%M")
            if waktu_tiba <= waktu_berangkat:
                print("[!] Waktu tiba harus setelah waktu berangkat!")
                continue  # Ulangi input waktu tiba
            break
        except ValueError:
            print("[!] Format waktu salah. Coba lagi, contoh: 06/30/2025 10:30")


    # Diubah ubah format waktunya dari datetime ke string supaya bisa disimpan di CSV
    waktu_berangkat_str = waktu_berangkat.strftime("%Y-%m-%d %H:%M")
    waktu_tiba_str = waktu_tiba.strftime("%Y-%m-%d %H:%M")
    
    jenis_kereta = input("Jenis Kereta: ")
    if batal_input(jenis_kereta): return
    
    # (incase si admin kelebihan input) limit dan minimal harga
    while True:
        harga = input("Harga Tiket: ")
        if batal_input(harga): return
        if harga.isdigit() and int(harga) > 0:
            harga = int(harga)
            if harga < 500 or harga > 100000:
                print("[!] Harga harus antara ¥500 dan ¥100.000. Coba lagi.")
            else:
                break
    
    # (incase si admin iseng nambahin negatif atau yang lainnya) validasi kursi 
    while True:
        kursi_tersedia = input("Jumlah Kursi Tersedia: ")
        if batal_input(kursi_tersedia): return
        if kursi_tersedia.isdigit() and int(kursi_tersedia) > 0:
            kursi_tersedia = int(kursi_tersedia)
            break
        else:
            print("[!] Jumlah kursi harus berupa angka positif. Coba lagi.")

    # Buat data baru untuk jadwal
    data_baru = {
        "id_jadwal": id_baru,
        "asal": asal,
        "tujuan": tujuan,
        "waktu_berangkat": waktu_berangkat_str,
        "waktu_tiba": waktu_tiba_str,
        "jenis_kereta": jenis_kereta,
        "harga": harga,
        "kursi_tersedia": kursi_tersedia
    }

    csv_handler.tambah_csv("jadwal.csv", data_baru, data_baru.keys())
    print("Jadwal baru berhasil ditambahkan!")
    lihat_jadwal()

# menu hapus jadwal
def hapus_jadwal():
    print("\n=== HAPUS JADWAL ===")
    data = csv_handler.baca_csv("jadwal.csv")

    if not data:
        print("[!] Tidak ada data jadwal.")
        return

    while True:
        print("\nJadwal Saat Ini:")
        tampilkan_jadwal(data)

        print("\nKetik ID jadwal yang ingin dihapus (contoh: J001,J002)")
        print("Ketik 0 untuk batal.")
        id_input = input("ID yang ingin dihapus: ")
        if batal_input(id_input): return

        # biar input id bisa lebih dari satu
        ids_hapus = [id.strip() for id in id_input.split(",")]
        id_ada = [row["id_jadwal"] for row in data]

        # Validasi ID yang ada di data
        id_valid = [id for id in ids_hapus if id in id_ada]
        id_invalid = [id for id in ids_hapus if id not in id_ada]

        if not id_valid:
            print("[!] Tidak ada ID yang cocok. Coba lagi.\n")
            continue

        # Proses penghapusan
        data_baru = [row for row in data if row["id_jadwal"] not in id_valid]

        # Simpan ulang ke file CSV
        csv_handler.tulis_csv("jadwal.csv", data_baru, data[0].keys())

        # Tambahkan ke file jadwal_terhapus.csv
        data_terhapus = [row for row in data if row["id_jadwal"] in id_valid]
        for row in data_terhapus:
            row["status"] = "Dihapus"
            row["dihapus_pada"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            csv_handler.tambah_csv("jadwal_terhapus.csv", row, row.keys())
        
        print(f"\nJadwal berikut berhasil dihapus: {', '.join(id_valid)}")
        if id_invalid:
            print(f"[!] ID berikut tidak ditemukan dan tidak dihapus: {', '.join(id_invalid)}")

        # Tampilkan hasil akhir
        print("\nJadwal Setelah Penghapusan:")
        tampilkan_jadwal(data_baru)
        break
    

# fungsi restore jadwal
def restore_jadwal():
    print("\n=== PULIHKAN JADWAL ===")
    data_aktif = csv_handler.baca_csv("jadwal.csv")
    data_hapus = csv_handler.baca_csv("jadwal_terhapus.csv")

    if not data_hapus:
        print("Belum ada jadwal yang bisa dipulihkan.")
        return

    # Tampilkan semua jadwal terhapus
    for i, row in enumerate(data_hapus, 1):
        print(f"{i}. {row['id_jadwal']} | {row['asal']} → {row['tujuan']} | "
              f"Dihapus pada: {row.get('dihapus_pada', '-')}")

    while True:
        restore_data = input("\nMasukkan ID jadwal yang ingin dipulihkan (contoh: J001,J002), atau 0 untuk batal: ").strip()
        if batal_input(restore_data): return

        ids_restore = [id.strip() for id in restore_data.split(",")]
        id_aktif = [row["id_jadwal"] for row in data_aktif]
        id_terhapus = [row["id_jadwal"] for row in data_hapus]

        id_valid = [id for id in ids_restore if id in id_terhapus and id not in id_aktif]
        id_invalid = [id for id in ids_restore if id not in id_terhapus]
        id_bentrok = [id for id in ids_restore if id in id_aktif]

        if not id_valid:
            print("[!] Tidak ada ID yang valid. Coba lagi.")
            if id_bentrok:
                print(f"↪ ID berikut sudah aktif: {', '.join(id_bentrok)}")
            if id_invalid:
                print(f"↪ ID berikut tidak ditemukan di data terhapus: {', '.join(id_invalid)}")
            continue

        # Data yang akan direstore
        data_restore = []
        for row in data_hapus:
            if row["id_jadwal"] in id_valid:
                # Buat row baru dengan field sesuai jadwal.csv
                row_cleaned = {key: row[key] for key in fieldnames_jadwal}
                data_restore.append(row_cleaned)

        # Tambahkan ke jadwal.csv (sekali banyak)
        csv_handler.tambah_csv("jadwal.csv", data_restore, fieldnames_jadwal)

        # Hapus dari data_hapus dan tulis ulang file jadwal_terhapus.csv
        data_hapus = [row for row in data_hapus if row["id_jadwal"] not in id_valid]
        csv_handler.tulis_csv("jadwal_terhapus.csv", data_hapus, fieldnames_terhapus)

        print(f"\nJadwal berhasil dipulihkan: {', '.join(id_valid)}")
        if id_bentrok:
            print(f"[!] Tidak dipulihkan karena sudah aktif: {', '.join(id_bentrok)}")
        if id_invalid:
            print(f"[!] Tidak dipulihkan karena tidak ditemukan: {', '.join(id_invalid)}")

        # Tampilkan jadwal terkini
        print("\n--- Jadwal Saat Ini ---")
        lihat_jadwal()
        break

# fungsi update kursi
def update_kursi_jadwal():
    print("\n=== UPDATE KURSI YANG HABIS ===")
    data = csv_handler.baca_csv("jadwal.csv")
    if not data:
        print("[!] Tidak ada jadwal yang tersedia.")
        return

    # Filter hanya yang kursinya habis
    kosong = [row for row in data if int(row["kursi_tersedia"]) == 0]
    if not kosong:
        print("[✓] Tidak ada jadwal dengan kursi 0.")
        return

    # Tampilkan daftar kursi 0
    for i, row in enumerate(kosong, 1):
        print(f"{i}. ID: {row['id_jadwal']} | {row['asal']} → {row['tujuan']} | "
              f"{row['waktu_berangkat']} | Kursi Sekarang: {row['kursi_tersedia']}")

    pilih = input("Masukkan nomor jadwal yang ingin diperbarui (0 untuk batal): ").strip()
    if batal_input(pilih): return

    try:
        idx = int(pilih) - 1
        if idx < 0 or idx >= len(kosong):
            raise ValueError
    except ValueError:
        print("[!] Nomor tidak valid.")
        return

    jadwal_dipilih = kosong[idx]
    id_target = jadwal_dipilih["id_jadwal"]

    # Input kursi baru
    while True:
        kursi_baru = input(f"Masukkan jumlah kursi baru untuk {id_target}: ").strip()
        if batal_input(kursi_baru): return
        if kursi_baru.isdigit() and int(kursi_baru) > 0:
            break
        else:
            print("[!] Input tidak valid. Masukkan angka positif.")

    # Update ke data asli
    for row in data:
        if row["id_jadwal"] == id_target:
            row["kursi_tersedia"] = kursi_baru
            break

    csv_handler.tulis_csv("jadwal.csv", data, data[0].keys())
    print(f"[✓] Kursi untuk jadwal {id_target} berhasil diperbarui jadi {kursi_baru}.")

# fungsi tampilan jadwal
def tampilkan_jadwal(data):
    if not data:
        print("Belum ada data jadwal.")
        return
    
    for i, row in enumerate(data, 1):
        print(f"{i}. {row['id_jadwal']} | {row['asal']} → {row['tujuan']} | "
              f"{row['waktu_berangkat']} - {row['waktu_tiba']} | "
              f"{row['jenis_kereta']} | Harga: ¥{row['harga']} | Kursi: {row['kursi_tersedia']}")

# buat liat jadwal
def lihat_jadwal():
    data = csv_handler.baca_csv("jadwal.csv")
    print("\n=== Daftar Jadwal ===")
    tampilkan_jadwal(data)


# jadwal buat user
def jadwal_user():
    print("\n=== JADWAL SHINKANSEN ===")
    print("(Data selalu ter-update berdasarkan perubahan dari Admin)\n")
    data = csv_handler.baca_csv("jadwal.csv")
    data_nonaktif = csv_handler.baca_csv("jadwal_terhapus.csv")
    tampilkan_jadwal(data)
    if data_nonaktif:
        print("\n--- [Jadwal Tidak Aktif / Dihapus oleh Admin] ---")
        for row in data_nonaktif:
            print(f"[Dihapus] {row['id_jadwal']} | {row['asal']} → {row['tujuan']} | "
                f"{row['waktu_berangkat']} - {row['waktu_tiba']} | {row['jenis_kereta']} | "
                f"Dihapus pada: {row.get('dihapus_pada','-')}")

def filter_jadwal():
    print("\n=== FILTER JADWAL ===")
    data = csv_handler.baca_csv("jadwal.csv")
    
    if not data:
        print("[!] Tidak ada jadwal yang tersedia.")
        return []

    asal = input("Masukkan stasiun asal (kosongkan untuk semua): ").strip()
    if batal_input(asal): return []
    tujuan = input("Masukkan stasiun tujuan (kosongkan untuk semua): ").strip()
    if batal_input(tujuan): return []

    data_terfilter = [
        row for row in data 
        if (asal.lower() in row['asal'].lower() or asal == '') and 
           (tujuan.lower() in row['tujuan'].lower() or tujuan == '')
    ]

    if not data_terfilter:
        print("[!] Tidak ada jadwal yang cocok dengan filter tersebut.")
        return []

    print("\n=== Hasil Filter Jadwal ===")
    tampilkan_jadwal(data_terfilter)
    return data_terfilter
