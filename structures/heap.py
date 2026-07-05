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
        self.heap = []  # array/list biasa sebagai representasi heap

    def is_empty(self):
        return len(self.heap) == 0

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # ---------------- INSERT ----------------
    def insert(self, pasien):
        """Menambahkan pasien baru ke heap lalu heapify up. O(log n)."""
        self.heap.append(pasien)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """Menaikkan elemen ke atas selama lebih prioritas dari parent-nya."""
        while i > 0:
            idx_parent = self._parent(i)
            if self.heap[i].tingkat_darurat < self.heap[idx_parent].tingkat_darurat:
                self._swap(i, idx_parent)
                i = idx_parent
            else:
                break

    # ---------------- DELETE ROOT ----------------
    def delete_root(self):
        """
        Mengambil & menghapus pasien paling darurat (root heap).
        O(log n).
        """
        if self.is_empty():
            return None
        akar = self.heap[0]
        elemen_terakhir = self.heap.pop()  # ambil elemen paling akhir
        if len(self.heap) > 0:
            self.heap[0] = elemen_terakhir
            self._heapify_down(0)
        return akar

    def _heapify_down(self, i):
        """Menurunkan elemen selama masih ada anak yang lebih prioritas."""
        n = len(self.heap)
        while True:
            kiri = self._left(i)
            kanan = self._right(i)
            terkecil = i

            if kiri < n and self.heap[kiri].tingkat_darurat < self.heap[terkecil].tingkat_darurat:
                terkecil = kiri
            if kanan < n and self.heap[kanan].tingkat_darurat < self.heap[terkecil].tingkat_darurat:
                terkecil = kanan

            if terkecil != i:
                self._swap(i, terkecil)
                i = terkecil
            else:
                break

    # ---------------- PEEK ----------------
    def peek(self):
        """Melihat pasien paling darurat tanpa menghapusnya. O(1)."""
        if self.is_empty():
            return None
        return self.heap[0]

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
