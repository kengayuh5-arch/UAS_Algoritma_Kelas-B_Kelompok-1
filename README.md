# UAS_Algoritma_Kelas-B_Kelompok-1
PROJECT UAS ALGORITMA  Implementasi Struktur Data pada Studi Kasus Nyata

# Sistem Manajemen UGD Rumah Sakit

Seluruh struktur data diimplementasikan **secara manual dari nol**
(tanpa `queue`, `collections.deque`, `heapq`, `PriorityQueue`, atau
library struktur data bawaan Python lainnya), murni menggunakan
Python standar tanpa dependensi eksternal.

## Struktur Proyek

```
sistem_ugd/
│
├── models/
│   └── pasien.py           # Class Pasien (blueprint data)
│
├── structures/
│   ├── queue.py             # Queue manual (antrean registrasi)
│   ├── stack.py              # Stack manual (riwayat tindakan / undo)
│   ├── bst.py                 # BST manual (database rawat inap)
│   └── heap.py                # Min-Heap manual (prioritas triase)
│
├── services/
│   └── sistem_ugd.py        # Integrasi seluruh struktur data
│
├── main.py                     # Entry point + menu CLI
└── README.md
```

## Alur Proses Bisnis

```
Registrasi Pasien        ->  Queue
        |
        v
Pemeriksaan / Triase     ->  Queue keluar -> Heap masuk
        |
        v
Penanganan Paling Darurat -> Heap keluar -> BST masuk + Stack (catat tindakan)
        |
        v
Lihat Database Rawat Inap -> BST (inorder traversal)

Undo Tindakan Terakhir    -> Stack (pop)
```

| Struktur Data | Peran dalam Sistem |
|---|---|
| **Queue** | Antrean registrasi pasien baru (FIFO) |
| **Binary Heap (Min-Heap)** | Penentuan prioritas penanganan berdasarkan tingkat kegawatan (triase) |
| **Binary Search Tree (BST)** | Database pasien rawat inap, key = `id_pasien` |
| **Stack** | Riwayat tindakan medis & mekanisme undo (LIFO) |

## Operasi yang Diimplementasikan

- **Queue** (`structures/queue.py`): `enqueue`, `dequeue`, `peek`, `display`
- **Stack** (`structures/stack.py`): `push`, `pop`, `peek`, `display`
- **BST** (`structures/bst.py`): `insert`, `search`, `delete`, `inorder_traversal`, `height`, `node_count`
  - `delete` digunakan pada menu **"Pasien Pulang / Keluar Rawat Inap"** — pasien yang sudah pulang dihapus dari database rawat inap
- **Binary Heap** (`structures/heap.py`): `insert`, `delete_root`, `peek`, `_heapify_up`, `_heapify_down`, `display`

## Alasan Pemilihan Traversal BST: Inorder

Inorder traversal pada BST dengan key `id_pasien` menghasilkan data
terurut menaik berdasarkan ID, sehingga cocok untuk menampilkan
daftar pasien rawat inap secara rapi dan mudah dibaca petugas.

## Alasan Pemilihan Min-Heap

`tingkat_darurat = 1` berarti **paling darurat**. Dengan Min-Heap,
nilai terkecil selalu berada di root sehingga pasien paling darurat
selalu diproses lebih dulu (`delete_root`).

## Analisis Kompleksitas Waktu (Big-O)

| Struktur Data | Operasi | Kompleksitas |
|---|---|---|
| Queue | enqueue, dequeue, peek | O(1) |
| Queue | display | O(n) |
| Stack | push, pop, peek | O(1) |
| Stack | display | O(n) |
| BST | insert, search, delete | O(log n) rata-rata, O(n) *worst-case* (skewed) |
| BST | inorder_traversal, height, | O(n) |
| BST | node_count | O(1) |
| Heap | insert, delete_root | O(log n) |
| Heap | peek | O(1) |