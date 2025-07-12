# ShinkansenTiketManager_IORI
Final Project for Data Structure (Semester 2)
# 🚄 SHINKs APP – Aplikasi Manajemen Pemesanan Tiket Shinkansen

SHINKs APP adalah aplikasi berbasis Python dengan antarmuka terminal yang memungkinkan pengguna untuk memesan tiket Shinkansen sebagai **akun** atau **guest**, serta menyediakan fitur admin untuk memantau dan mengelola seluruh data.

---

## ✨ Fitur Utama
### 👥 Multi-Level User Access
- **Admin**
  - (Harus pakai password kalau mau mengakses menu Admin)
  - Manajemen jadwal (tambah, hapus, restore, update kursi)
  - Manajemen penumpang
  - Konfirmasi tiket & refund
  - Laporan penjualan
- **User Akun (Login)**
  - Pesan tiket dengan saldo akun
  - Cek & top-up saldo
  - Riwayat pemesanan
  - Ajukan refund
- **Guest**
  - Pesan tiket tanpa login
    
---

## 📁 Struktur Folder
- `database/` → Semua file .csv untuk data
  - `database/jadwal.csv/jadwal_terhapus.csv/` → sudah otomatis terupdate setiap admin manage jadwal
- `Login.py/` → tampilan sebagai Admin or User (dah bikin fitur buat akun)
- `main.py` → Menu utama aplikasi CLI
- `Admin/` → Tampilan Admin jika login sebagai Admin
  - ada penambahan fitur berupa `konfirmasi.py/` yang dimana digunakan untuk mengkonfirmasi pemesanan-pemesanan user berakun maupun guest
  - `fitur1/` → Jadwal
  - `fitur4/` → Manajemen Penumpang
  - `fitur5/` → Laporan Penjualan
- `fitur6/` → Refund (bisa Admin "konfirmasi" & User "Pengajuan")
- `User/` → Tampilan User jika login sebagai User
  - (Buat jadwal nya bakal otomatis update dan cuman view-only)
  - `fitur2/` → Pemesanan Tiket
  - `fitur3/` → Pencarian & Filter
- `utils/` → File-File yang membantu di program project ini
- `utils.akun_user/` → ada fungsi buat_akun kalo mau bikin akun


---

## 📦 Daftar Fitur Lengkap
### 🧑‍💼 Menu Admin
- Manajemen Jadwal: Tambah, Hapus, dan Pulihkan jadwal, Update Kursi
- Konfirmasi Tiket: Memindahkan data pemesanan ke data terkonfirmasi
- Konfirmasi Refund: Memproses pengajuan refund dan mengembalikan saldo/kursi
- Laporan Penjualan: Ringkasan tiket terjual, pendapatan, total pemesanan dan penumpang per tanggal

### 👤 Menu User (Login)
- Lihat Jadwal & Filter
- Pesan Tiket: Bayar dari saldo
- Cek Saldo
- Top-up Saldo
- Riwayat Pemesanan
- Ajukan Refund

### 👥 Menu Guest
- Lihat Jadwal
- Pesan Tiket tanpa akun
- (Hanya yang punya akun yang bisa refund)

---

## 🧾 File CSV yang Digunakan

| File                          | Deskripsi                                         |
| ----------------------------- | ------------------------------------------------- |
| `akun_user.csv`               | Data akun user (username, password, saldo, email) |
| `jadwal.csv`                  | Jadwal Shinkansen aktif                           |
| `jadwal_terhapus.csv`         | Jadwal yang sudah dihapus admin                   |
| `pemesanan_akun.csv`          | Pemesanan oleh user yang login                    |
| `pemesanan_guest.csv`         | Pemesanan oleh guest                              |
| `pemesanan_terkonfirmasi.csv` | Data pemesanan yang telah dikonfirmasi admin      |
| `penumpang.csv`               | Data penumpang yang pernah melakukan pemesanan    |
| `refund.csv`                  | Data pengajuan refund                             |
| `laporan.csv`                 | Laporan penjualan harian                          |

---

## 🛠️ Requirements

- Python 3.10+ (rekomendasi: Python 3.12)
- Berjalan di terminal (CLI)
- Tidak membutuhkan library eksternal tambahan (hanya modul bawaan)

---

## 🚀 Cara Menjalankan

1. Pastikan semua file `.csv` berada di direktori project yang sama.
2. Jalankan aplikasi dari file `main.py`:

```bash
python main.py