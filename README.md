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