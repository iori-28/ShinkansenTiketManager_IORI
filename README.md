# ShinkansenTiketManager_IORI
Project iseng

## Struktur Folder
- `database/` → Semua file .csv untuk data
  - `database/jadwal.csv/jadwal_terhapus.csv/` → sudah otomatis terupdate setiap admin manage jadwal
- `Login.py/` → tampilan sebagai Admin or User (dah bikin fitur buat akun)
- `main.py` → Menu utama aplikasi CLI
- `Admin/` → Tampilan Admin jika login sebagai Admin
  - ada penambahan fitur berupa `konfirmasi.py/` yang dimana digunakan untuk mengkonfirmasi pemesanan-pemesanan user berakun maupun guest
  - `fitur1/` → Jadwal (UDAAAAAH)
  - `fitur4/` → Manajemen Penumpang
  - `fitur5/` → Laporan Penjualan
- `fitur6/` → Refund (bisa Admin & User)
- `User/` → Tampilan User jika login sebagai User
  - (Buat jadwal nya bakal otomatis update dan cuman view-only)
  - Ada penambahan `akun_user.py/` di utils
  - `fitur2/` → Pemesanan Tiket
  - `fitur3/` → Pencarian & Filter
- `utils/` → File-File yang membantu di program project ini
