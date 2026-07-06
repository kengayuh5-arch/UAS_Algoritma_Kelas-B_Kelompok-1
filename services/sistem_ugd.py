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


class CatatanTindakan:
    """
    Pembungkus data yang disimpan di Stack (riwayat_tindakan).

    Kenapa perlu dibungkus, bukan cuma teks polos?
    Karena saat UNDO dilakukan, sistem perlu tahu JENIS tindakan apa
    yang dibatalkan, supaya bisa membalikkan EFEK NYATA-nya di struktur
    data lain (bukan cuma menghapus catatan teksnya saja).

    Atribut:
        tipe       : "TINDAKAN" (tindakan medis biasa) atau "PULANG" (pasien keluar dari BST)
        pasien     : objek Pasien terkait
        keterangan : deskripsi tindakan/kejadian
    """

    def __init__(self, tipe, pasien, keterangan):
        self.tipe = tipe
        self.pasien = pasien
        self.keterangan = keterangan

    def __str__(self):
        # Format tampilan dibuat SAMA seperti sebelumnya, supaya display()
        # Stack tidak perlu diubah sama sekali
        return f"ID:{self.pasien.id_pasien} ({self.pasien.nama}) -> {self.keterangan}"


class SistemUGD:
    """
    Mengintegrasikan Queue, Heap, BST, dan Stack dalam satu alur
    proses bisnis UGD.
    """

    def __init__(self):
        self.antrean_registrasi = Queue()     # Queue -> menyimpan pasien yang baru daftar, belum ditriase
        self.heap_triase = MinHeapTriase()    # Binary Heap -> menyimpan pasien yang sudah ditriase, menunggu ditangani
        self.db_rawat_inap = BST()            # Binary Search Tree -> database permanen pasien yang sudah ditangani
        self.riwayat_tindakan = Stack()       # Stack -> log tindakan medis, bisa di-undo
        self._counter_id = 1                  # generator id_pasien otomatis, naik terus setiap registrasi baru

    # ---------- MENU 1: REGISTRASI PASIEN BARU (-> QUEUE) ----------
    def registrasi_pasien(self):
        print("\n=== REGISTRASI PASIEN BARU ===")
        nama = input("Nama pasien   : ").strip()
        gejala = input("Gejala/keluhan: ").strip()

        # tingkat_darurat masih None karena pasien BELUM diperiksa/ditriase
        pasien_baru = Pasien(self._counter_id, nama, gejala, tingkat_darurat=None)
        self._counter_id += 1     # siapkan id untuk pasien berikutnya

        self.antrean_registrasi.enqueue(pasien_baru)   # << TITIK MASUK KE QUEUE
        print(f"\n[OK] Pasien '{nama}' (ID:{pasien_baru.id_pasien}) berhasil "
              f"didaftarkan dan masuk ke antrean registrasi.")

    # ---------- MENU 2: TRIASE (QUEUE -> HEAP) ----------
    def triase_pasien(self):
        print("\n=== PEMERIKSAAN AWAL (TRIASE) ===")
        if self.antrean_registrasi.is_empty():
            print("[INFO] Antrean registrasi kosong. Tidak ada pasien untuk ditriase.")
            return

        pasien = self.antrean_registrasi.dequeue()   # << TITIK KELUAR DARI QUEUE
        # setelah dequeue, urutan kedatangan pasien ini sudah tidak relevan lagi
        print(f"Memeriksa pasien: {pasien}")

        while True:
            try:
                tingkat = int(input("Tentukan tingkat darurat (1=Paling darurat .. 5=Ringan): "))
                if 1 <= tingkat <= 5:
                    break
                print("[ERROR] Masukkan angka antara 1 sampai 5.")
            except ValueError:
                print("[ERROR] Input harus berupa angka.")

        pasien.tingkat_darurat = tingkat            # isi prioritas hasil pemeriksaan
        self.heap_triase.insert(pasien)              # << TITIK MASUK KE HEAP
        # sekarang urutan penanganan ditentukan tingkat kegawatan, bukan lagi urutan datang
        print(f"\n[OK] Pasien '{pasien.nama}' (ID:{pasien.id_pasien}) telah "
              f"ditriase dengan tingkat darurat {tingkat} dan masuk ke heap prioritas.")

    # ---------- MENU 3: TANGANI PASIEN PALING DARURAT (HEAP -> BST + STACK) ----------
    def tangani_pasien_darurat(self):
        print("\n=== TANGANI PASIEN PALING DARURAT ===")
        if self.heap_triase.is_empty():
            print("[INFO] Tidak ada pasien di heap triase yang menunggu penanganan.")
            return

        pasien = self.heap_triase.delete_root()   # << TITIK KELUAR DARI HEAP (selalu yang PALING darurat)
        print(f"Menangani pasien paling darurat: {pasien}")

        tindakan = input("Masukkan deskripsi tindakan medis yang diberikan: ").strip()

        # Setelah ditangani, pasien dicatat PERMANEN sebagai pasien rawat inap
        self.db_rawat_inap.insert(pasien)          # << TITIK MASUK KE BST

        # Tindakan yang diberikan dicatat sebagai riwayat, supaya bisa di-undo
        # kalau ternyata ada salah input. Tipe "TINDAKAN" berarti undo-nya
        # nanti CUKUP menghapus catatan ini saja (tidak ada perubahan lain
        # yang perlu dibalik, karena pasien memang seharusnya tetap di BST)
        catatan = CatatanTindakan(tipe="TINDAKAN", pasien=pasien, keterangan=tindakan)
        self.riwayat_tindakan.push(catatan)         # << TITIK MASUK KE STACK

        print(f"\n[OK] Pasien '{pasien.nama}' telah ditangani, dicatat sebagai "
              f"rawat inap (BST), dan tindakan dicatat ke riwayat (Stack).")

    # ---------- MENU 4: LIHAT DATABASE RAWAT INAP (BST) ----------
    def lihat_database_rawat_inap(self):
        print("\n=== DATABASE PASIEN RAWAT INAP (BST - Inorder Traversal) ===")
        self.db_rawat_inap.display()   # tampil terurut ID karena pakai inorder traversal

    # ---------- MENU 5: UNDO TINDAKAN TERAKHIR (STACK) ----------
    def undo_tindakan(self):
        print("\n=== BATALKAN (UNDO) TINDAKAN TERAKHIR ===")
        if self.riwayat_tindakan.is_empty():
            print("[INFO] Tidak ada riwayat tindakan untuk dibatalkan.")
            return

        catatan = self.riwayat_tindakan.pop()   # << TITIK KELUAR DARI STACK
        # pop() otomatis ambil yang PALING BARU dimasukkan (sifat LIFO) -> cocok untuk undo

        if catatan.tipe == "PULANG":
            # Efek nyata yang harus dibalik: pasien tadi dihapus dari BST
            # saat dipulangkan -> sekarang harus di-INSERT KEMBALI ke BST
            self.db_rawat_inap.insert(catatan.pasien)
            print(f"[OK] Tindakan berikut telah dibatalkan (undo):\n   {catatan}")
            print(f"[OK] Pasien '{catatan.pasien.nama}' (ID:{catatan.pasien.id_pasien}) "
                  f"telah DIKEMBALIKAN ke database rawat inap (BST).")
        else:
            # Tipe "TINDAKAN": tidak ada struktur data lain yang perlu
            # dibalik, karena pasien memang seharusnya tetap tercatat di
            # BST terlepas dari tindakan medis spesifik ini. Cukup hapus
            # catatannya saja dari riwayat.
            print(f"[OK] Tindakan berikut telah dibatalkan (undo):\n   {catatan}")

    # ---------- MENU TAMBAHAN: LIHAT STATUS SEMUA STRUKTUR DATA ----------
    def lihat_status_sistem(self):
        # Menu ini tidak mengubah data apapun, cuma menampilkan isi
        # keempat struktur data sekaligus untuk keperluan demo/cek
        print("\n=== STATUS SELURUH STRUKTUR DATA SAAT INI ===")
        print("\n[1] QUEUE - Antrean Registrasi")
        self.antrean_registrasi.display()

        print("\n[2] BINARY HEAP - Prioritas Triase")
        self.heap_triase.display()

        print("\n[3] BINARY SEARCH TREE - Database Rawat Inap")
        self.db_rawat_inap.display()

        print("\n[4] STACK - Riwayat Tindakan Medis")
        self.riwayat_tindakan.display()

    # ---------- MENU 6: PASIEN PULANG / KELUAR RAWAT INAP (HAPUS DARI BST) ----------
    def pasien_pulang(self):
        print("\n=== PASIEN PULANG (KELUAR DARI RAWAT INAP) ===")
        if self.db_rawat_inap.node_count() == 0:
            print("[INFO] Tidak ada pasien rawat inap saat ini.")
            return

        try:
            id_pulang = int(input("Masukkan ID pasien yang akan dipulangkan: "))
        except ValueError:
            print("[ERROR] ID harus berupa angka.")
            return

        # cari dulu datanya SEBELUM dihapus, supaya nama pasien masih bisa
        # ditampilkan/dicatat setelah node-nya hilang dari BST
        pasien = self.db_rawat_inap.search(id_pulang)
        if pasien is None:
            print(f"[INFO] Pasien dengan ID {id_pulang} tidak ditemukan di database rawat inap.")
            return

        berhasil = self.db_rawat_inap.delete(id_pulang)   # << TITIK KELUAR DARI BST (operasi delete)
        if berhasil:
            # Tipe "PULANG" ditandai secara eksplisit, supaya kalau nanti
            # di-undo, sistem tahu harus meng-INSERT KEMBALI pasien ini
            # ke BST (bukan cuma menghapus catatan tekstualnya saja)
            catatan = CatatanTindakan(
                tipe="PULANG",
                pasien=pasien,
                keterangan="PULANG / Keluar dari rawat inap"
            )
            self.riwayat_tindakan.push(catatan)
            print(f"\n[OK] Pasien '{pasien.nama}' (ID:{pasien.id_pasien}) telah "
                  f"dipulangkan dan dihapus dari database rawat inap (BST).")
        else:
            print("[ERROR] Gagal menghapus data pasien.")

    # ---------- MENU TAMBAHAN: CARI PASIEN DI BST ----------
    def cari_pasien(self):
        print("\n=== CARI PASIEN RAWAT INAP (BST) ===")
        try:
            id_cari = int(input("Masukkan ID pasien yang dicari: "))
        except ValueError:
            print("[ERROR] ID harus berupa angka.")
            return
        hasil = self.db_rawat_inap.search(id_cari)   # manfaatkan search BST -> O(log n) rata-rata
        if hasil is None:
            print(f"[INFO] Pasien dengan ID {id_cari} tidak ditemukan di database rawat inap.")
        else:
            print(f"[OK] Pasien ditemukan: {hasil}")
