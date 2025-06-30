# utils/helper.py
def batal_input(teks_input: str) -> bool:
    """
    Mengecek apakah input bernilai "0", jika ya tampilkan pesan dan return True.
    """
    if teks_input.strip() == "0":
        print("Proses dibatalkan.")
        return True
    return False
