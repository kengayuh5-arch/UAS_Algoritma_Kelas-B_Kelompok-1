"""
main.py

ENTRY POINT - SISTEM MANAJEMEN UGD RUMAH SAKIT
UAS Algoritma dan Struktur Data

Menjalankan menu CLI utama yang menggunakan SistemUGD (services/sistem_ugd.py)
untuk mengintegrasikan Queue, Stack, Binary Search Tree, dan Binary Heap.

Cara menjalankan:
    python main.py
"""

from services.sistem_ugd import SistemUGD
# File ini SENGAJA tidak berisi logika struktur data/algoritma apapun.
# Tugasnya murni menampilkan menu dan meneruskan pilihan user ke method
# yang sesuai di SistemUGD. Ini memisahkan "tampilan" dari "logika bisnis".


def tampilkan_menu():
    print("\n" + "=" * 60)
    print("   SISTEM MANAJEMEN UGD RUMAH SAKIT")
    print("=" * 60)
    print("1. Registrasi Pasien Baru             (masuk ke Queue)")
    print("2. Pemeriksaan Awal / Triase           (Queue -> Heap)")
    print("3. Tangani Pasien Paling Darurat       (Heap -> BST + Stack)")
    print("4. Lihat Database Pasien Rawat Inap    (tampilkan BST)")
    print("5. Batalkan Tindakan Terakhir / Undo   (pop Stack)")
    print("6. Pasien Pulang / Keluar Rawat Inap   (delete BST)")
    print("7. Cari Pasien di Database Rawat Inap  (search BST)")
    print("8. Lihat Status Seluruh Struktur Data")
    print("0. Keluar")
    print("=" * 60)


def main():
    sistem = SistemUGD()    # 1 objek yang membungkus keempat struktur data
    print("Selamat datang di Sistem Manajemen UGD Rumah Sakit.")

    while True:                                   # loop menu, terus berjalan sampai user pilih "0"
        tampilkan_menu()
        pilihan = input("Pilih menu (0-8): ").strip()

        # setiap pilihan tinggal memanggil method yang sudah dibuat
        # di services/sistem_ugd.py -> main.py tidak perlu tahu
        # detail cara kerja Queue/Stack/BST/Heap di dalamnya
        if pilihan == "1":
            sistem.registrasi_pasien()
        elif pilihan == "2":
            sistem.triase_pasien()
        elif pilihan == "3":
            sistem.tangani_pasien_darurat()
        elif pilihan == "4":
            sistem.lihat_database_rawat_inap()
        elif pilihan == "5":
            sistem.undo_tindakan()
        elif pilihan == "6":
            sistem.pasien_pulang()
        elif pilihan == "7":
            sistem.cari_pasien()
        elif pilihan == "8":
            sistem.lihat_status_sistem()
        elif pilihan == "0":
            print("\nTerima kasih. Program selesai.")
            break        # keluar dari loop while, program berakhir
        else:
            print("[ERROR] Pilihan tidak valid, silakan coba lagi.")


if __name__ == "__main__":
    # baris ini memastikan main() hanya berjalan kalau file ini dijalankan
    # langsung (python main.py), bukan saat di-import file lain
    main()
