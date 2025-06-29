import csv
import os

# Path ke folder database
BASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database')

def full_path(filename):
    return os.path.join(BASE_PATH, filename)

def baca_csv(nama_file):
    try:
        with open(full_path(nama_file), mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"[!] File {nama_file} tidak ditemukan.")
        return []

def tulis_csv(nama_file, data, fieldnames):
    with open(full_path(nama_file), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def tambah_csv(nama_file, data_baru, fieldnames):
    file_path = full_path(nama_file)
    file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data_baru)
