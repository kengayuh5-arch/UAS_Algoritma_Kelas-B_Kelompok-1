"""
services/sistem_ugd.py

KELAS INTEGRASI: SistemUGD

Menghubungkan keempat struktur data dalam satu alur proses bisnis:

    Registrasi (Queue) -> Triase (masuk ke Heap) -> Penanganan pasien
    paling darurat (keluar dari Heap, masuk ke BST) -> Tindakan medis
    dicatat ke Stack -> Undo tindakan terakhir bila diperlukan (Stack)
"""

from models.pasien import Pasien
from structures.queue import Queue
from structures.stack import Stack
from structures.bst import BST
from structures.heap import MinHeapTriase


class SistemUGD:
    """
    Mengintegrasikan Queue, Heap, BST, dan Stack dalam satu alur
    proses bisnis UGD.
    """

    def __init__(self):
        self.antrean_registrasi = Queue()     # Queue
        self.heap_triase = MinHeapTriase()    # Binary Heap
        self.db_rawat_inap = BST()            # Binary Search Tree
        self.riwayat_tindakan = Stack()       # Stack
        self._counter_id = 1                  # generator id_pasien otomatis

    # ---------- MENU 1: REGISTRASI PASIEN BARU (-> QUEUE) ----------
    def registrasi_pasien(self):
        print("\n=== REGISTRASI PASIEN BARU ===")
        nama = input("Nama pasien   : ").strip()
        gejala = input("Gejala/keluhan: ").strip()

        pasien_baru = Pasien(self._counter_id, nama, gejala, tingkat_darurat=None)
        self._counter_id += 1

        self.antrean_registrasi.enqueue(pasien_baru)
        print(f"\n[OK] Pasien '{nama}' (ID:{pasien_baru.id_pasien}) berhasil "
              f"didaftarkan dan masuk ke antrean registrasi.")

    # ---------- MENU 2: TRIASE (QUEUE -> HEAP) ----------
    def triase_pasien(self):
        print("\n=== PEMERIKSAAN AWAL (TRIASE) ===")
        if self.antrean_registrasi.is_empty():
            print("[INFO] Antrean registrasi kosong. Tidak ada pasien untuk ditriase.")
            return

        pasien = self.antrean_registrasi.dequeue()
        print(f"Memeriksa pasien: {pasien}")

        while True:
            try:
                tingkat = int(input("Tentukan tingkat darurat (1=Paling darurat .. 5=Ringan): "))
                if 1 <= tingkat <= 5:
                    break
                print("[ERROR] Masukkan angka antara 1 sampai 5.")
            except ValueError:
                print("[ERROR] Input harus berupa angka.")

        pasien.tingkat_darurat = tingkat
        self.heap_triase.insert(pasien)
        print(f"\n[OK] Pasien '{pasien.nama}' (ID:{pasien.id_pasien}) telah "
              f"ditriase dengan tingkat darurat {tingkat} dan masuk ke heap prioritas.")

    # ---------- MENU 3: TANGANI PASIEN PALING DARURAT (HEAP -> BST + STACK) ----------
    def tangani_pasien_darurat(self):
        print("\n=== TANGANI PASIEN PALING DARURAT ===")
        if self.heap_triase.is_empty():
            print("[INFO] Tidak ada pasien di heap triase yang menunggu penanganan.")
            return

        pasien = self.heap_triase.delete_root()
        print(f"Menangani pasien paling darurat: {pasien}")

        tindakan = input("Masukkan deskripsi tindakan medis yang diberikan: ").strip()

        # Masukkan ke BST sebagai pasien rawat inap
        self.db_rawat_inap.insert(pasien)

        # Catat tindakan ke Stack (untuk riwayat / undo)
        catatan = f"ID:{pasien.id_pasien} ({pasien.nama}) -> {tindakan}"
        self.riwayat_tindakan.push(catatan)

        print(f"\n[OK] Pasien '{pasien.nama}' telah ditangani, dicatat sebagai "
              f"rawat inap (BST), dan tindakan dicatat ke riwayat (Stack).")

    # ---------- MENU 4: LIHAT DATABASE RAWAT INAP (BST) ----------
    def lihat_database_rawat_inap(self):
        print("\n=== DATABASE PASIEN RAWAT INAP (BST - Inorder Traversal) ===")
        self.db_rawat_inap.display()

    # ---------- MENU 5: UNDO TINDAKAN TERAKHIR (STACK) ----------
    def undo_tindakan(self):
        print("\n=== BATALKAN (UNDO) TINDAKAN TERAKHIR ===")
        if self.riwayat_tindakan.is_empty():
            print("[INFO] Tidak ada riwayat tindakan untuk dibatalkan.")
            return
        tindakan_dibatalkan = self.riwayat_tindakan.pop()
        print(f"[OK] Tindakan berikut telah dibatalkan (undo):\n   {tindakan_dibatalkan}")

    # ---------- MENU TAMBAHAN: LIHAT STATUS SEMUA STRUKTUR DATA ----------
    def lihat_status_sistem(self):
        print("\n=== STATUS SELURUH STRUKTUR DATA SAAT INI ===")
        print("\n[1] QUEUE - Antrean Registrasi")
        self.antrean_registrasi.display()

        print("\n[2] BINARY HEAP - Prioritas Triase")
        self.heap_triase.display()

        print("\n[3] BINARY SEARCH TREE - Database Rawat Inap")
        self.db_rawat_inap.display()

        print("\n[4] STACK - Riwayat Tindakan Medis")
        self.riwayat_tindakan.display()

    # ---------- MENU TAMBAHAN: CARI PASIEN DI BST ----------
    def cari_pasien(self):
        print("\n=== CARI PASIEN RAWAT INAP (BST) ===")
        try:
            id_cari = int(input("Masukkan ID pasien yang dicari: "))
        except ValueError:
            print("[ERROR] ID harus berupa angka.")
            return
        hasil = self.db_rawat_inap.search(id_cari)
        if hasil is None:
            print(f"[INFO] Pasien dengan ID {id_cari} tidak ditemukan di database rawat inap.")
        else:
            print(f"[OK] Pasien ditemukan: {hasil}")
