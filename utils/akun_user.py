# utils/user_account.py
import csv
import os
from utils.helper import batal_input
from utils import csv_handler
from utils.csv_handler import full_path

AKUN_USER_PATH = full_path("akun_user.csv")

# Daftar user baru
def daftar_akun():
    print("\n=== REGISTRASI AKUN ===")
    print("Ketik 0 kapan saja untuk membatalkan proses.")

    akun = []
    if os.path.exists(AKUN_USER_PATH):
        with open(AKUN_USER_PATH, newline='', encoding='utf-8') as file:
            akun = list(csv.DictReader(file))

    while True:
        username = input("Username: ").strip()
        if batal_input(username): return
        if username == "":
            print("[!] Username tidak boleh kosong.")
            continue

        if any(user['username'] == username for user in akun):
            print(f"[!] Username '{username}' sudah digunakan. Pilih yang lain.")
        else:
            break

    password = input("Password: ").strip()
    if batal_input(password): return

    nama = input("Nama Lengkap: ").strip()
    if batal_input(nama): return

    email = input("Email: ").strip()
    if batal_input(email): return

    user_baru = {
        "username": username,
        "password": password,
        "nama": nama,
        "email": email,
        "saldo": "0"
    }

    with open(AKUN_USER_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=user_baru.keys())
        if os.stat(AKUN_USER_PATH).st_size == 0:
            writer.writeheader()
        writer.writerow(user_baru)

    print(f"\nRegistrasi berhasil! Selamat datang, {nama}. Saldo awal: ¥0")
    return username

# Login user
def login_user():
    print("\n=== LOGIN USER ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        with open(AKUN_USER_PATH, newline='', encoding='utf-8') as file:
            akun = list(csv.DictReader(file))
    except FileNotFoundError:
        print("[!] Belum ada akun terdaftar.")
        return None

    for user in akun:
        if user['username'] == username and user['password'] == password:
            print(f"\nLogin berhasil!.")
            return username

    print("[!] Username atau password salah.")
    return None

# cek saldo user
def cek_saldo(username):
    users = csv_handler.baca_csv("akun_user.csv")
    for user in users:
        if user["username"] == username:
            print(f"Saldo Anda: ¥{user['saldo']}")
            return
    print("[!] Akun tidak ditemukan.")

# topup saldo user
def topup_saldo(username):
    users = csv_handler.baca_csv("akun_user.csv")
    ditemukan = False

    for user in users:
        if user["username"] == username:
            ditemukan = True
            print(f"Saldo saat ini: ¥{user['saldo']}")
            while True:
                jumlah = input("Masukkan jumlah top-up (angka positif): ")
                if batal_input(jumlah): return
                elif jumlah.isdigit() and int(jumlah) > 0:
                    user["saldo"] = str(int(user["saldo"]) + int(jumlah))
                    csv_handler.tulis_csv("akun_user.csv", users, users[0].keys())
                    print(f"Top-up berhasil! Saldo baru Anda: ¥{user['saldo']}")
                    return
                else:
                    print("[!] Input tidak valid. Masukkan angka positif.")
    
    if not ditemukan:
        print("[!] Username tidak ditemukan.")