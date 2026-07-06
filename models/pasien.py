"""
models/pasien.py

Blueprint (class) objek Pasien yang dialirkan ke semua struktur data
(Queue, Heap, BST) dalam Sistem Manajemen UGD.
"""


class Pasien:
    """
    Atribut:
        id_pasien      : int  -> digunakan sebagai key di BST
        nama           : str
        gejala         : str
        tingkat_darurat: int (1-5) -> 1 = PALING DARURAT (dipakai
                          sebagai prioritas di Binary Heap; semakin
                          kecil angkanya, semakin diprioritaskan)
    """

    def __init__(self, id_pasien, nama, gejala, tingkat_darurat=None):
        self.id_pasien = id_pasien              # key unik, dipakai BST untuk insert/search/delete
        self.nama = nama                         # nama pasien, hanya untuk ditampilkan
        self.gejala = gejala                     # keluhan awal saat registrasi
        self.tingkat_darurat = tingkat_darurat   # key prioritas, dipakai Heap. None dulu saat
                                                  # registrasi, baru diisi angka 1-5 setelah triase

    def __str__(self):
        # Method ini otomatis dipanggil setiap kali objek Pasien di-print()
        # atau dimasukkan ke f-string, supaya tampilannya rapi (bukan
        # <Pasien object at 0x...> bawaan Python)
        return (f"[ID:{self.id_pasien}] {self.nama} | Gejala: {self.gejala} "
                f"| Tingkat Darurat: {self.tingkat_darurat}")
