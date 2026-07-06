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
        self.id_pasien = id_pasien
        self.nama = nama
        self.gejala = gejala
        self.tingkat_darurat = tingkat_darurat

    def __str__(self):
        return (f"[ID:{self.id_pasien}] {self.nama} | Gejala: {self.gejala} "
                f"| Tingkat Darurat: {self.tingkat_darurat}")
