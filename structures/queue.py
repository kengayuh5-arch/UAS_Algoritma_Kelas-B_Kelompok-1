"""
structures/queue.py

QUEUE (ANTREAN REGISTRASI PASIEN) - Implementasi manual dengan
Linked List (TIDAK menggunakan collections.deque atau queue bawaan
Python).

Operasi wajib: enqueue, dequeue, peek, display
Kompleksitas: enqueue O(1), dequeue O(1), peek O(1), display O(n)
"""


class _NodeQueue:
    """Node internal untuk linked list pada Queue."""

    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """Queue (FIFO) diimplementasikan dengan Linked List manual."""

    def __init__(self):
        self.head = None   # elemen paling depan (akan di-dequeue duluan)
        self.tail = None   # elemen paling belakang (tempat enqueue)
        self._size = 0

    def is_empty(self):
        return self.head is None

    def enqueue(self, data):
        """Menambahkan pasien baru ke belakang antrean. O(1)."""
        node_baru = _NodeQueue(data)
        if self.is_empty():
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru
        self._size += 1

    def dequeue(self):
        """Mengeluarkan pasien paling depan antrean. O(1)."""
        if self.is_empty():
            return None
        node_keluar = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return node_keluar.data

    def peek(self):
        """Melihat pasien paling depan tanpa mengeluarkannya. O(1)."""
        if self.is_empty():
            return None
        return self.head.data

    def display(self):
        """Menampilkan seluruh isi antrean dari depan ke belakang. O(n)."""
        if self.is_empty():
            print("   (Antrean registrasi kosong)")
            return
        print("   --- Antrean Registrasi (depan -> belakang) ---")
        current = self.head
        posisi = 1
        while current is not None:
            print(f"   {posisi}. {current.data}")
            current = current.next
            posisi += 1

    def size(self):
        return self._size
