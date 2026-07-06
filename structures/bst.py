"""
structures/bst.py

BINARY SEARCH TREE (BST) - DATABASE PASIEN RAWAT INAP
Implementasi manual (TIDAK menggunakan library Binary Tree bawaan).
Key yang digunakan untuk penyusunan tree: id_pasien.

Operasi wajib: insert, search, delete, traversal, height, node_count
Kompleksitas rata-rata O(log n), worst-case O(n) jika tree tidak
seimbang (skewed).

Alasan pemilihan traversal INORDER:
    Inorder traversal pada BST yang menggunakan id_pasien sebagai key
    akan menghasilkan urutan data terurut menaik berdasarkan ID. Ini
    cocok untuk kebutuhan menampilkan daftar pasien rawat inap secara
    rapi dan terurut, memudahkan pencarian visual oleh petugas.
"""


class _NodeBST:
    # Setiap node BST punya maksimal 2 anak: left (lebih kecil) dan
    # right (lebih besar/sama). Ini yang membentuk "pohon"-nya.
    def __init__(self, pasien):
        self.pasien = pasien   # objek Pasien yang disimpan di node ini
        self.left = None        # anak kiri: subtree berisi id_pasien LEBIH KECIL
        self.right = None        # anak kanan: subtree berisi id_pasien LEBIH BESAR/SAMA


class BST:
    """Binary Search Tree manual untuk data pasien rawat inap."""

    def __init__(self):
        self.root = None            # titik teratas tree, None kalau tree masih kosong
        self._jumlah_node = 0        # counter manual, supaya node_count() tidak perlu hitung ulang O(n)

    # input/insert
    def insert(self, pasien):
        """Menyisipkan pasien baru berdasarkan id_pasien. O(log n) rata2."""
        if self.root is None:
            self.root = _NodeBST(pasien)      # tree kosong -> pasien baru langsung jadi root
        else:
            self._insert_rekursif(self.root, pasien)   # tree sudah ada isi -> cari posisi lewat rekursi
        self._jumlah_node += 1

    def _insert_rekursif(self, node, pasien):
        # LOGIKA INTI BST: membandingkan id_pasien baru dengan node saat ini
        if pasien.id_pasien < node.pasien.id_pasien:
            # id lebih kecil -> harus masuk ke subtree KIRI
            if node.left is None:
                node.left = _NodeBST(pasien)          # slot kosong ditemukan, taruh di sini
            else:
                self._insert_rekursif(node.left, pasien)  # masih ada isi, turun lagi lebih dalam
        else:
            # id lebih besar/sama -> harus masuk ke subtree KANAN
            if node.right is None:
                node.right = _NodeBST(pasien)
            else:
                self._insert_rekursif(node.right, pasien)

    # search
    def search(self, id_pasien):
        """Mencari pasien berdasarkan id_pasien. O(log n) rata2."""
        return self._search_rekursif(self.root, id_pasien)

    def _search_rekursif(self, node, id_pasien):
        if node is None:
            return None                          # sudah mentok ujung tree, data tidak ditemukan
        if node.pasien.id_pasien == id_pasien:
            return node.pasien                    # ditemukan! langsung kembalikan
        elif id_pasien < node.pasien.id_pasien:
            return self._search_rekursif(node.left, id_pasien)   # cari di subtree kiri
        else:
            return self._search_rekursif(node.right, id_pasien)  # cari di subtree kanan
        # Inilah kenapa BST lebih cepat dari list biasa: setiap langkah
        # membuang SEPARUH kemungkinan (mirip logika binary search)

    # delete
    def delete(self, id_pasien):
        """Menghapus pasien (misal sudah dipulangkan) dari BST. O(log n) rata2."""
        self.root, berhasil = self._delete_rekursif(self.root, id_pasien)
        if berhasil:
            self._jumlah_node -= 1
        return berhasil

    def _delete_rekursif(self, node, id_pasien):
        if node is None:
            return node, False    # data tidak ditemukan, tidak ada yang dihapus

        # Tahap 1: cari dulu node yang mau dihapus (sama seperti search)
        if id_pasien < node.pasien.id_pasien:
            node.left, berhasil = self._delete_rekursif(node.left, id_pasien)
        elif id_pasien > node.pasien.id_pasien:
            node.right, berhasil = self._delete_rekursif(node.right, id_pasien)
        else:
            # Node yang dicari SUDAH KETEMU (id_pasien == node saat ini).
            # Ada 3 KEMUNGKINAN KASUS penghapusan node BST:

            # KASUS 1: node tidak punya anak kiri (bisa juga tidak punya anak sama sekali)
            # -> tinggal "lompati" node ini, sambungkan parent langsung ke anak kanannya
            if node.left is None:
                return node.right, True

            # KASUS 2: node tidak punya anak kanan (tapi punya anak kiri)
            # -> sambungkan parent langsung ke anak kirinya
            elif node.right is None:
                return node.left, True

            # KASUS 3: node punya DUA anak -> paling rumit.
            # Tidak bisa langsung dihapus karena akan memutus 2 cabang sekaligus.
            # Solusi: cari "successor" (nilai TERKECIL di subtree KANAN),
            # karena nilai itu pasti lebih besar dari semua yang di kiri
            # dan lebih kecil dari semua sisa yang di kanan -> aman menggantikan posisi ini.
            else:
                successor = self._cari_minimum(node.right)   # cari pengganti
                node.pasien = successor.pasien                # ganti data node ini dengan data successor
                # lalu hapus successor yang asli dari posisi lamanya (pasti masuk Kasus 1,
                # karena node paling kiri tidak mungkin punya anak kiri)
                node.right, _ = self._delete_rekursif(node.right, successor.pasien.id_pasien)
                return node, True

        return node, berhasil

    def _cari_minimum(self, node):
        # Nilai terkecil pada BST SELALU berada di ujung paling kiri
        while node.left is not None:
            node = node.left
        return node

    #traversal inorder
    def inorder_traversal(self):
        """Mengembalikan list pasien terurut menaik berdasarkan ID. O(n)."""
        hasil = []
        self._inorder_rekursif(self.root, hasil)
        return hasil

    def _inorder_rekursif(self, node, hasil):
        # Urutan kunjungan: KIRI -> NODE -> KANAN
        if node is not None:
            self._inorder_rekursif(node.left, hasil)   # 1. kunjungi semua yang lebih kecil dulu
            hasil.append(node.pasien)                    # 2. baru catat node ini sendiri
            self._inorder_rekursif(node.right, hasil)   # 3. baru kunjungi semua yang lebih besar
        # Karena aturan BST (kiri < node < kanan), urutan Kiri->Node->Kanan
        # ini OTOMATIS menghasilkan data terurut menaik tanpa perlu sorting tambahan

    #height
    def height(self):
        """Menghitung tinggi tree (jumlah level tertinggi). O(n)."""
        return self._height_rekursif(self.root)

    def _height_rekursif(self, node):
        if node is None:
            return -1   # tree kosong dianggap tinggi -1, supaya 1 node (tanpa anak) hasilnya height 0
        tinggi_kiri = self._height_rekursif(node.left)     # hitung tinggi subtree kiri
        tinggi_kanan = self._height_rekursif(node.right)    # hitung tinggi subtree kanan
        return 1 + max(tinggi_kiri, tinggi_kanan)    # ambil yang PALING TINGGI di antara keduanya, +1 untuk node ini sendiri

    # node count
    def node_count(self):
        """Menghitung jumlah total node dalam tree. O(1) (disimpan counter)."""
        return self._jumlah_node   # tidak perlu hitung ulang seluruh tree, cukup baca counter

    def display(self):
        """Menampilkan seluruh pasien rawat inap secara terurut (inorder)."""
        hasil = self.inorder_traversal()
        if not hasil:
            print("   (Belum ada pasien rawat inap)")
            return
        print("   --- Database Pasien Rawat Inap (terurut ID - Inorder) ---")
        for pasien in hasil:
            print(f"   - {pasien}")
        print(f"   Jumlah node : {self.node_count()}")
        print(f"   Tinggi tree : {self.height()}")
