# ShinkansenTiketManager_IORI
Tugas Struktur Data membuat aplikasi manajemen 

## Struktur Folder
- `database/` → Semua file .csv untuk data
- `Login.py/` → tampilan sebagai (Admin or Consumen)
- `main.py` → Menu utama aplikasi CLI
- `Admin/` → Tampilan Admin jika login sebagai Admin
  - `fitur1/` → Manajemen Jadwal
  - `fitur4/` → Manajemen Penumpang
  - `fitur5/` → Laporan Penjualan
- `fitur6/` → Refund (bisa Admin & Consumer)
- `Consumer/` → Tampilan Consumer jika login sebagai Consumer
  - `fitur2/` → Pemesanan Tiket
  - `fitur3/` → Pencarian & Filter
- `utils/` → Handler CSV & Struktur Data