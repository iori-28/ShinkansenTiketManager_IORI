# buat di jadwal
fieldnames_jadwal = [
    'id_jadwal','asal','tujuan','waktu_berangkat',
    'waktu_tiba','jenis_kereta','harga','kursi_tersedia'
    ]

#buat hapus jadwal
fieldnames_terhapus = fieldnames_jadwal + ['status', 'dihapus_pada']

# buat di pemesanan
fieldnames_pemesanan = [
    "id_pemesanan", "id_penumpang", "nama_penumpang", "email_penumpang",
    "id_jadwal", "jumlah_tiket", "total_harga", "status",
    "waktu_pesan", "waktu_konfirmasi", "tipe"
]

# buat refund
fieldnames_refund = [
    "id_refund", "id_pemesanan", "nama_penumpang", "email_penumpang",
    "alasan", "waktu_refund", "jumlah_refund"
]

# buat manajemen penumpang
fieldnames_penumpang = [
    'id_penumpang', 'nama_penumpang',
    'email_penumpang', 'user_SHINKs',
    'waktu_pesan'
]
