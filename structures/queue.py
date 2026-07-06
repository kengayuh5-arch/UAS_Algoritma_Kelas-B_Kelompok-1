"""
structures/queue.py

QUEUE (ANTREAN REGISTRASI PASIEN) - Implementasi manual dengan
Linked List (TIDAK menggunakan collections.deque atau queue bawaan
Python).

Operasi wajib: enqueue, dequeue, peek, display
Kompleksitas: enqueue O(1), dequeue O(1), peek O(1), display O(n)
"""


class _NodeQueue:
    # Unit terkecil dari linked list. Setiap node menyimpan 1 data
    # (objek Pasien) dan pointer "next" yang menunjuk ke node berikutnya.
    def __init__(self, data):
        self.data = data   # data yang disimpan (objek Pasien)
        self.next = None    # pointer ke node berikutnya, None = belum tersambung ke apa-apa


class Queue:
    """Queue (FIFO) diimplementasikan dengan Linked List manual."""

    def __init__(self):
        self.head = None    # penanda elemen PALING DEPAN (yang akan keluar duluan saat dequeue)
        self.tail = None    # penanda elemen PALING BELAKANG (tempat data baru masuk saat enqueue)
        self._size = 0       # jumlah elemen saat ini, supaya size() tidak perlu hitung ulang O(n)

    def is_empty(self):
        # Queue dianggap kosong kalau head belum menunjuk ke node manapun
        return self.head is None

    def enqueue(self, data):
        """Menambahkan pasien baru ke belakang antrean. O(1)."""
        node_baru = _NodeQueue(data)      # bungkus data ke dalam node baru
        if self.is_empty():
            # Kasus khusus: queue masih kosong -> node baru sekaligus jadi head dan tail
            self.head = node_baru
            self.tail = node_baru
        else:
            # Kasus umum: sambungkan node lama (tail) ke node baru,
            # lalu geser tail ke node baru itu
            self.tail.next = node_baru
            self.tail = node_baru
        self._size += 1   # tambah counter ukuran

    def dequeue(self):
        """Mengeluarkan pasien paling depan antrean. O(1)."""
        if self.is_empty():
            return None                    # tidak ada yang bisa dikeluarkan
        node_keluar = self.head            # simpan referensi node paling depan (yang akan dikeluarkan)
        self.head = self.head.next         # geser head ke node berikutnya
        if self.head is None:
            # Penting: kalau setelah geser ternyata head jadi None,
            # berarti queue sudah kosong -> tail WAJIB direset juga,
            # supaya enqueue berikutnya tidak nyambung ke node "yatim" yang sudah dihapus
            self.tail = None
        self._size -= 1
        return node_keluar.data             # kembalikan data pasien yang dikeluarkan

    def peek(self):
        """Melihat pasien paling depan tanpa mengeluarkannya. O(1)."""
        if self.is_empty():
            return None
        return self.head.data     # cuma baca data head, tidak mengubah struktur apapun

    def display(self):
        """Menampilkan seluruh isi antrean dari depan ke belakang. O(n)."""
        if self.is_empty():
            print("   (Antrean registrasi kosong)")
            return
        print("   --- Antrean Registrasi (depan -> belakang) ---")
        current = self.head        # mulai penelusuran dari head
        posisi = 1
        while current is not None:
            print(f"   {posisi}. {current.data}")
            current = current.next  # pindah ke node berikutnya
            posisi += 1
        # loop berhenti otomatis saat current == None (sudah sampai ujung list)

    def size(self):
        return self._size
