"""
structures/heap.py

BINARY HEAP (MIN-HEAP) - PENENTUAN PRIORITAS TRIASE
Implementasi manual berbasis array/list Python biasa
(TIDAK menggunakan heapq atau PriorityQueue bawaan Python).

Operasi wajib: insert, delete_root, peek, heapify_up, heapify_down, display
Kompleksitas: insert O(log n), delete_root O(log n), peek O(1)

Alasan Min-Heap:
    tingkat_darurat = 1 berarti PALING darurat. Dengan Min-Heap, nilai
    terkecil selalu berada di root, sehingga pasien paling darurat
    selalu berada di posisi teratas dan bisa ditangani lebih dulu.
"""


class MinHeapTriase:
    """Min-Heap manual berbasis array untuk prioritas triase pasien."""

    def __init__(self):
        self.heap = []   # array/list biasa yang merepresentasikan tree heap
        # Catatan: heap TIDAK pakai pointer/node seperti BST. Hubungan
        # parent-child cukup dihitung dari POSISI INDEX di array ini.

    def is_empty(self):
        return len(self.heap) == 0

    # ----- Rumus posisi index: inti representasi array sebagai tree -----
    def _parent(self, i):
        return (i - 1) // 2   # parent dari index i

    def _left(self, i):
        return 2 * i + 1        # anak kiri dari index i

    def _right(self, i):
        return 2 * i + 2         # anak kanan dari index i

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]   # tukar posisi 2 elemen

    # ---------------- INSERT ----------------
    def insert(self, pasien):
        """Menambahkan pasien baru ke heap lalu heapify up. O(log n)."""
        self.heap.append(pasien)                 # taruh dulu di posisi PALING AKHIR array
        self._heapify_up(len(self.heap) - 1)      # baru "naikkan" kalau ternyata lebih prioritas dari parent-nya

    def _heapify_up(self, i):
        """Menaikkan elemen ke atas selama lebih prioritas dari parent-nya."""
        while i > 0:                              # ulangi selama belum sampai root (index 0)
            idx_parent = self._parent(i)
            if self.heap[i].tingkat_darurat < self.heap[idx_parent].tingkat_darurat:
                # elemen ini LEBIH DARURAT (angka lebih kecil) dari parent-nya
                # -> tidak boleh, harus ditukar posisi supaya lebih darurat ada di atas
                self._swap(i, idx_parent)
                i = idx_parent                     # lanjut cek lagi dari posisi barunya (mungkin masih perlu naik lagi)
            else:
                break                                # sudah sesuai aturan Min-Heap, berhenti

    # ---------------- DELETE ROOT ----------------
    def delete_root(self):
        """
        Mengambil & menghapus pasien paling darurat (root heap).
        O(log n).
        """
        if self.is_empty():
            return None
        akar = self.heap[0]                     # root (index 0) = pasien PALING DARURAT, ini yang akan diambil
        elemen_terakhir = self.heap.pop()         # ambil sekaligus buang elemen paling akhir array
        if len(self.heap) > 0:
            # pindahkan elemen terakhir tadi ke posisi root yang kosong,
            # lalu "turunkan" ke posisi yang benar
            self.heap[0] = elemen_terakhir
            self._heapify_down(0)
        return akar

    def _heapify_down(self, i):
        """Menurunkan elemen selama masih ada anak yang lebih prioritas."""
        n = len(self.heap)
        while True:
            kiri = self._left(i)
            kanan = self._right(i)
            terkecil = i                          # asumsi awal: node ini sendiri yang paling darurat

            # bandingkan dengan anak kiri (kalau ada)
            if kiri < n and self.heap[kiri].tingkat_darurat < self.heap[terkecil].tingkat_darurat:
                terkecil = kiri
            # bandingkan juga dengan anak kanan (kalau ada)
            # -> WAJIB cek dua-duanya, kalau cuma cek salah satu bisa salah
            #    pilih anak yang ditukar dan merusak aturan Min-Heap
            if kanan < n and self.heap[kanan].tingkat_darurat < self.heap[terkecil].tingkat_darurat:
                terkecil = kanan

            if terkecil != i:
                # ternyata ada anak yang lebih darurat -> tukar posisi, lalu lanjut turun dari sana
                self._swap(i, terkecil)
                i = terkecil
            else:
                break   # node sudah lebih darurat dari kedua anaknya (atau sudah jadi daun), berhenti

    # ---------------- PEEK ----------------
    def peek(self):
        """Melihat pasien paling darurat tanpa menghapusnya. O(1)."""
        if self.is_empty():
            return None
        return self.heap[0]   # root selalu di index 0, tidak perlu pencarian apapun

    def display(self):
        """Menampilkan seluruh isi heap (urutan array internal)."""
        if self.is_empty():
            print("   (Tidak ada pasien menunggu penanganan di heap triase)")
            return
        print("   --- Heap Triase (urutan internal array, root = paling darurat) ---")
        for i, pasien in enumerate(self.heap):
            tanda = " <-- ROOT (akan ditangani duluan)" if i == 0 else ""
            print(f"   [{i}] {pasien}{tanda}")

    def size(self):
        return len(self.heap)
