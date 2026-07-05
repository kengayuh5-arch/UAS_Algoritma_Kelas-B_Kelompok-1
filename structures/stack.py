"""
structures/stack.py

STACK (RIWAYAT TINDAKAN MEDIS / UNDO) - Implementasi manual dengan
Linked List (TIDAK menggunakan library bawaan Python).

Operasi wajib: push, pop, peek, display
Kompleksitas: push O(1), pop O(1), peek O(1), display O(n)
"""


class _NodeStack:
    """Node internal untuk linked list pada Stack."""

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """Stack (LIFO) diimplementasikan dengan Linked List manual."""

    def __init__(self):
        self.top = None
        self._size = 0

    def is_empty(self):
        return self.top is None

    def push(self, data):
        """Menambahkan tindakan baru ke puncak stack. O(1)."""
        node_baru = _NodeStack(data)
        node_baru.next = self.top
        self.top = node_baru
        self._size += 1

    def pop(self):
        """Mengeluarkan (membatalkan/undo) tindakan paling atas. O(1)."""
        if self.is_empty():
            return None
        node_keluar = self.top
        self.top = self.top.next
        self._size -= 1
        return node_keluar.data

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
        current = self.top
        posisi = 1
        while current is not None:
            print(f"   {posisi}. {current.data}")
            current = current.next
            posisi += 1

    def size(self):
        return self._size
