"""
structures/stack.py

STACK (RIWAYAT TINDAKAN MEDIS / UNDO) - Implementasi manual dengan
Linked List (TIDAK menggunakan library bawaan Python).

Operasi wajib: push, pop, peek, display
Kompleksitas: push O(1), pop O(1), peek O(1), display O(n)
"""


class _NodeStack:
    # Sama seperti node di Queue, bedanya di sini cukup 1 pointer arah
    # karena Stack cuma butuh akses dari 1 ujung (atas/top)
    def __init__(self, data):
        self.data = data
        self.next = None   # menunjuk ke node DI BAWAHNYA (yang masuk lebih dulu)


class Stack:
    """Stack (LIFO) diimplementasikan dengan Linked List manual."""

    def __init__(self):
        self.top = None    # penanda elemen PALING ATAS (satu-satunya titik akses push/pop)
        self._size = 0

    def is_empty(self):
        return self.top is None

    def push(self, data):
        """Menambahkan tindakan baru ke puncak stack. O(1)."""
        node_baru = _NodeStack(data)
        node_baru.next = self.top   # node baru "menunjuk" ke top lama (yang sekarang ada di bawahnya)
        self.top = node_baru          # top dipindah ke node baru -> node terbaru selalu paling atas
        self._size += 1

    def pop(self):
        """Mengeluarkan (membatalkan/undo) tindakan paling atas. O(1)."""
        if self.is_empty():
            return None
        node_keluar = self.top        # simpan referensi node paling atas
        self.top = self.top.next      # geser top ke node di bawahnya
        self._size -= 1
        return node_keluar.data        # kembalikan data yang "dibatalkan"

    def peek(self):
        """Melihat tindakan paling atas tanpa mengeluarkannya. O(1)."""
        if self.is_empty():
            return None
        return self.top.data

    def display(self):
        """Menampilkan seluruh riwayat tindakan dari yang terbaru. O(n)."""
        if self.is_empty():
            print("   (Belum ada riwayat tindakan)")
            return
        print("   --- Riwayat Tindakan (terbaru -> terlama) ---")
        current = self.top     # mulai dari top (yang paling baru dimasukkan)
        posisi = 1
        while current is not None:
            print(f"   {posisi}. {current.data}")
            current = current.next  # turun ke node berikutnya (lebih lama)
            posisi += 1
        # Catatan penting: karena mulai dari top, urutan tampilan otomatis
        # dari yang PALING BARU ke yang PALING LAMA -> ini yang membedakan
        # Stack (LIFO) dari Queue (FIFO)

    def size(self):
        return self._size
