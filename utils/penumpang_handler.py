# utils/penumpang_handler.py
from utils import csv_handler
from utils.fieldnames import fieldnames_penumpang

def simpan_data_penumpang(data):
    """
    Menyimpan data penumpang ke dalam penumpang.csv
    data: dict berisi id_penumpang, nama_penumpang, email_penumpang, user_SHINKs, waktu_pesan
    """
    if not all(field in data for field in fieldnames_penumpang):
        print("[!] Data penumpang tidak lengkap. Gagal disimpan.")
        return

    csv_handler.tambah_csv("penumpang.csv", data, fieldnames_penumpang)
