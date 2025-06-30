# ShinkansenTiketManager_IORI
Tugas Struktur Data membuat aplikasi manajemen 

## Struktur Folder
- `database/` → Semua file .csv untuk data
  - `database/jadwal.csv/jadwal_terhapus.csv/` → sudah otomatis terupdate setiap admin manage jadwal
- `Login.py/` → tampilan sebagai Admin or User (baru login admin, bingung yang user mau pake akun apa engga karna nanti ada laporan, history, dan penumpang di bagian admin)
- `main.py` → Menu utama aplikasi CLI
- `Admin/` → Tampilan Admin jika login sebagai Admin
  - `fitur1/` → Jadwal (UDAAAAAH)
  - `fitur4/` → Manajemen Penumpang
  - `fitur5/` → Laporan Penjualan
- `fitur6/` → Refund (bisa Admin & Consumer)
- `Consumer/` → Tampilan Consumer jika login sebagai Consumer
  - (Buat jadwal nya bakal otomatis update dan cuman view-only)
  - `fitur2/` → Pemesanan Tiket
  - `fitur3/` → Pencarian & Filter
- `utils/` → File-File yang membantu di program project ini