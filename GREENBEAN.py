import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate

def header():
    os.system('cls')
    with open('Header.txt', 'r', encoding='UTF-8') as file:
            filetxt = file.read()
    print(filetxt)

def register():
    print("========== REGISTER AKUN BARU ==========")
    username = input("Masukkan username baru: ")
    password = input("Masukkan password baru: ")

    print("\nPilih role Anda:")
    print("1. Penjual")
    print("2. Pembeli")
    role_input = input("Masukkan angka (1/2): ")

    if role_input == "1":
        role = "Penjual"
    elif role_input == "2":
        role = "Pembeli"
    else:
        print("Pilihan salah!")
        return None, None

    try:
        df = pd.read_csv("Users.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Username", "Password", "Role"])

    if username in list(df["Username"]):
        print("Username sudah digunakan!")
        return None, None

    df.loc[len(df)] = [username, password, role]
    df.to_csv("Users.csv", index=False)

    print(f"Akun '{username}' berhasil didaftarkan!\n")
    return username, role

def login():
    try:
        df = pd.read_csv("Users.csv")
    except FileNotFoundError:
        print("File Users.csv tidak ditemukan!")
        return None, None

    df.set_index("Username", inplace=True)

    print("\n=== LOGIN ===")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    if username not in df.index:
        print("Username tidak ditemukan!")
        return None, None

    if password != str(df.loc[username, "Password"]):
        print("Password salah!")
        return None, None

    role = df.loc[username, "Role"]
    print(f"\nLogin berhasil! Halo {role}")
    return username, role

def lihatProduk(username):
    try:
        df = pd.read_csv("dataEdamame.csv")
    except FileNotFoundError:
        print("File dataEdamame.csv tidak ditemukan!")
        return
    data = df[df["Nama Toko"] == username]
    if data.empty:
        print("Belum ada produk untuk toko ini.")
        return
    data_list = [[row["Nama Toko"], row["Produk"], row["Stok"], f"Rp{row['Harga Lokal']}", f"Rp{row['Harga Ekspor']}"] for _, row in data.iterrows()]
    print(tabulate(data_list, headers=["Nama Toko","Produk","Stok","Harga Lokal","Harga Ekspor"], tablefmt="fancy_grid"))


def tambahProduk(username):
    print("\n========== TAMBAH PRODUK ==========")
    produk = input("Nama produk: ")
    stok = float(input("Stok (kg): "))
    hargaLokal = float(input("Harga Lokal: "))
    hargaEkspor = float(input("Harga Ekspor: "))
    try:
        df = pd.read_csv("dataEdamame.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Nama Toko","Produk","Stok","Harga Lokal","Harga Ekspor"])
    df_new = pd.DataFrame({"Nama Toko":[username],"Produk":[produk],"Stok":[stok],"Harga Lokal":[hargaLokal],"Harga Ekspor":[hargaEkspor]})
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_csv("dataEdamame.csv", index=False)
    print("Produk berhasil ditambahkan!\n")


def ubahData(username):
    try:
        df = pd.read_csv('dataEdamame.csv')
    except:
        print("Data belum ada!")
        return

    data = df[df["Nama Toko"] == username]
    data_list = [[idx, row["Nama Toko"],row["Produk"],row["Stok"],f"Rp{row['Harga Lokal']}",f"Rp{row['Harga Ekspor']}" ]for idx, row in data.iterrows()]

    print(tabulate(data_list, headers=["Index", "Nama Toko", "Produk", "Stok", "Harga Lokal", "Harga Ekspor"], tablefmt="fancy_grid"))
    pilih = int(input("Masukkan index produk yang ingin diubah: "))

    index_list = [row[0] for row in data_list]

    if pilih not in index_list:
        print("Index tidak valid!")
        return
    else:
        produk = input("Nama produk baru: ")
        stok = int(input("Stok baru: "))
        hargaLokal = int(input("Harga Lokal baru: "))
        hargaEkspor = int(input("Harga Ekspor baru: "))
        df.loc[pilih, "Produk"] = produk
        df.loc[pilih, "Stok"] = stok
        df.loc[pilih, "Harga Lokal"] = hargaLokal
        df.loc[pilih, "Harga Ekspor"] = hargaEkspor

        df.to_csv("dataEdamame.csv", index=False)
        print("Data berhasil diubah!")


def hapusData(username):
    try:
        df = pd.read_csv('dataEdamame.csv')
    except:
        print("Belum ada data!")
        return

    data = df[df["Nama Toko"] == username]
    print(tabulate(data.reset_index(), headers=["Nama Toko", "Produk", "Stok", "Harga Lokal", "Harga Ekspor"], tablefmt="fancy_grid"))

    try:
        pilih = int(input("Masukkan index produk yang ingin dihapus: "))
    except:
        print("Input harus angka!")
        return

    if pilih not in data.index:
        print("Index tidak valid!")
        return

    df = df.drop(pilih)
    df = df.reset_index(drop=True)
    df.to_csv('dataEdamame.csv', index=False)

    print("Produk berhasil dihapus!")

def simpan_riwayatPenjualan(pesanan_list, total_bayar, nama_pembeli, nama_toko, metode_pembayaran):
    if not pesanan_list:
        return
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    riwayat_baru = []
    for item in pesanan_list:
        riwayat_baru.append({
            "Waktu": waktu,
            "Pembeli": nama_pembeli,
            "Toko": item["toko"],
            "Produk": item["produk"],
            "Jenis": item["jenis"],
            "Berat": float(item["berat"]),
            "Harga Total": float(item["harga_total"]),
            "Total Bayar": float(total_bayar),
            "Pembayaran" : metode_pembayaran
        })
    try:
        df = pd.read_csv("riwayatpenjualan.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=["Waktu","Pembeli","Toko","Produk","Jenis","Berat","Harga Total","Total Bayar", "Metode Pembayaran"])
    df = pd.concat([df,pd.DataFrame(riwayat_baru)], ignore_index=True)
    df.to_csv("riwayatpenjualan.csv", index=False, encoding="utf-8-sig")
    print("Riwayat penjualan berhasil disimpan!")

def lihatRiwayat_Penjualan(username):
    try:
        df = pd.read_csv("riwayatpenjualan.csv")

        if df.empty:
            print("Belum ada riwayat transaksi.")
            return

        data_toko = df[df["Toko"] == username]

        if data_toko.empty:
            print(f"Belum ada transaksi untuk toko '{username}'.")
            return

        data_list = []
        for _, row in data_toko.iterrows():
            data_list.append([row["Pembeli"],row["Produk"],row["Jenis"],row["Berat"],f"Rp{row['Harga Total']:,}",f"Rp{row['Total Bayar']:,}",row["Waktu"], row["Pembayaran"] ])

        print("\n=== RIWAYAT PENJUALAN TOKO ANDA ===")
        print(tabulate(
            data_list,
            headers=["Pembeli", "Produk", "Jenis","Berat", "Harga Total", "Total Bayar", "Waktu", "Pembayaran"],tablefmt="fancy_grid"))

    except FileNotFoundError:
        print("Belum ada riwayat transaksi (file tidak ditemukan).")


def buat_permintaan(username, nama_toko):
    file_path = "permintaanPembeli.csv"

    try:
        df = pd.read_csv(file_path)
    except:
        df = pd.DataFrame(columns=["Pembeli", "Produk", "Jumlah (kg)", "Keterangan", "Tanggal Permintaan", "Toko"])

    produk = input("Nama produk yang ingin diminta: ")

    while True:
        try:
            jumlah = float(input("Jumlah (kg): "))
            break
        except ValueError:
            print("Jumlah harus angka!")

    keterangan = input("Keterangan (opsional): ")
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    permintaan_baru = {
        "Pembeli": username,
        "Produk": produk,
        "Jumlah (kg)": jumlah,
        "Keterangan": keterangan if keterangan != "" else "Tidak ada",
        "Tanggal Permintaan": tanggal,
        "Toko": nama_toko   # ← WAJIB!
    }

    df = pd.concat([df, pd.DataFrame([permintaan_baru])], ignore_index=True)
    df.to_csv(file_path, index=False)

    print("Permintaan berhasil dicatat!")




def lihatPermintaan_Pembeli(username_penjual):
    try:
        df = pd.read_csv('permintaanPembeli.csv')
        if df.empty:
            print("Belum ada permintaan.")
            return

        if "Toko" not in df.columns:
            print("FORMAT FILE SALAH: Kolom 'Toko' belum ada.")
            print("Hapus permintaanPembeli.csv agar dibuat ulang dengan format baru.")
            return

        df_toko = df[df["Toko"] == username_penjual]

        if df_toko.empty:
            print("Belum ada permintaan untuk toko Anda.")
            return

        data_list = [
            [row["Pembeli"], row["Produk"], row["Jumlah (kg)"], row["Keterangan"], row["Tanggal Permintaan"]]
            for _, row in df_toko.iterrows()
        ]

        print(tabulate(
            data_list,
            headers=["Pembeli", "Produk", "Jumlah (kg)", "Keterangan", "Tanggal"],
            tablefmt="fancy_grid"
        ))

    except FileNotFoundError:
        print("Belum ada permintaan.")
    except pd.errors.EmptyDataError:
        print("Belum ada permintaan.")


def tampilan_toko (toko_df):
    print("\n==========Daftar Toko==========")
    toko = toko_df["Nama Toko"].unique()
    toko_list = [[i+1, toko] for i, toko in enumerate (toko)]
    print(tabulate(toko_list, headers=["No", "Toko"], tablefmt="fancy_grid"))
    return toko

def pilih_toko(toko_df):
    toko = tampilan_toko(toko_df)
    while True:
        try:
            pilihan = int(input("\nPilih nomor toko: "))
            if 1<= pilihan <= len(toko):
                return toko[pilihan -1]
            else:
                print("Pilihan tidak valid")
        except ValueError:
            print("Input harus berupa angka")

def tampilan_produk(produk_df, toko):
    print(f"\n=== Produk di Toko{toko.capitalize()}===")
    toko_produk = produk_df[produk_df["Nama Toko"].str.lower()==toko.lower()]
    if not toko_produk.empty:
        produk_list = [[row["No"], row["Produk"], row["Stok"], f"Rp{row['Harga Lokal']}", f"Rp{row['Harga Ekspor']}"]for _, row in toko_produk.iterrows()]

        print(tabulate(produk_list, headers=["No", "Produk", "Stok", "Harga Lokal", "Harga Ekspor"], tablefmt="fancy_grid"))
    else:
        print("Tidak ada produk")

def lihat_produk_toko(df, toko_terpilih):
    toko_produk = df[df["Nama Toko"] == toko_terpilih]

    if toko_produk.empty:
        print("Toko ini belum memiliki produk.")
        return pd.DataFrame()

    data_list = [
        [i+1, row["Nama Toko"], row["Produk"], row["Stok"], f"Rp{row['Harga Lokal']}", f"Rp{row['Harga Ekspor']}"]
        for i, (_, row) in enumerate(toko_produk.iterrows())
    ]

    print(tabulate(data_list,
                   headers=["No", "Nama Toko", "Produk", "Stok", "Harga Lokal", "Harga Ekspor"],
                   tablefmt="fancy_grid",
                   showindex=False))
    
    return toko_produk



def beliproduk(produk_df, username,  toko_terpilih):
    total_belanja = 0
    total_berat = 0
    daftar_pesanan = []
    toko_produk = produk_df[produk_df["Nama Toko"] == toko_terpilih]

    try:
        pilih_produk = int(input("Pilih nomor produk: ")) - 1
        row = toko_produk.iloc[pilih_produk]
        
    except:
        print("Produk tidak valid!")
        return total_belanja, total_berat, daftar_pesanan

    produk = row["Produk"]
    stok_tersedia = row["Stok"]

    print("\n=== PILIH JENIS HARGA ===")
    print("1. Lokal")
    print("2. Ekspor")
    jenis = input("Pilih (1/2): ")

    if jenis == "1":
        harga_kg = row["Harga Lokal"]
        jenis_harga = "Lokal"
    elif jenis == "2":
        harga_kg = row["Harga Ekspor"]
        jenis_harga = "Ekspor"
    else:
        print("Input tidak valid!")
        return total_belanja, total_berat, daftar_pesanan

    try:
        berat = float(input(f"Masukkan berat (kg) untuk {produk}: "))
    except ValueError:
        print("Berat harus angka!")
        return total_belanja, total_berat, daftar_pesanan

    if berat > stok_tersedia:
            print(f"\n Stok {produk} hanya tersisa {stok_tersedia} kg.")
            if berat > stok_tersedia:
                print(f"\n Stok {produk} hanya tersisa {stok_tersedia} kg.")
                while True:
                    opsi = input("Apakah ingin membuat permintaan untuk sisanya? (y/n): ").lower()
                    if opsi == 'y':
                        sisa = berat - stok_tersedia
                        print(f"Membuat permintaan untuk {sisa} kg {produk}...")
                        buat_permintaan(username, toko_terpilih)
                        berat = stok_tersedia  
                        break
                    elif opsi == 'n':
                        print("Batal membeli lebih dari stok, silakan pilih jumlah lain.")
                        break
                    else:
                        print("Input salah, ketik y atau n.")
                    if opsi == 'n':
                        continue 

    total_item = harga_kg * berat
    total_belanja += total_item
    total_berat += berat

    df = pd.read_csv("dataEdamame.csv")
    index_produk = df[(df["Nama Toko"] == toko_terpilih) & (df["Produk"] == produk)].index[0]
    df.loc[index_produk, "Stok"] -= berat
    df.to_csv("dataEdamame.csv", index=False)

    daftar_pesanan.append({
        "produk": produk,
        "jenis": jenis_harga,
        "berat": berat,
        "harga_per_kg": harga_kg,
        "harga_total": total_item,
        "toko": toko_terpilih
    })

    print(f"\n✓ {produk} {berat} kg ({jenis_harga}) ditambahkan. Total: Rp{total_item:,}")
    print(f"TOTAL BELANJA: Rp{total_belanja:,}")

    return total_belanja, total_berat, daftar_pesanan


def hitung_ongkir(berat_paket):   
    
    print(f"\nTotal Berat Paket Belanja Anda: {berat_paket:.2f} Kg")
    print("=== PILIH TUJUAN PENGIRIMAN ===")
    
    tujuan = input("Masukkan Tujuan (Domestik/Internasional): ").capitalize()
    
    harga_per_kg = 0
    valid_input = True 

    if tujuan == "Domestik":
        zona = input("Masukkan Zona (Jawa/Luar Jawa): ").capitalize()
        if zona == "Jawa":
            harga_per_kg = 6000 if berat_paket <= 5 else 5000 
        elif zona == "Luar jawa": 
            harga_per_kg = 10000 if berat_paket <= 5 else 8500
        else:
            print("Zona tidak valid untuk Domestik.")
            valid_input = False
    elif tujuan == "Internasional":
        zona = input("Masukkan Zona (Asia Tenggara/Benua Lain): ").capitalize()
        if zona == "Asia tenggara": 
            harga_per_kg = 40000 if berat_paket <= 5 else 35000
        elif zona == "Benua lain": 
            harga_per_kg = 75000 if berat_paket <= 5 else 68000
        else:
            print("Zona tidak valid untuk Internasional.")
            valid_input = False
    else:
        print("Tujuan tidak valid.")
        valid_input = False

    if not valid_input:
        return 0, 0, tujuan, zona                           

    total_biaya_ongkir = berat_paket * harga_per_kg         
    return total_biaya_ongkir, harga_per_kg, tujuan, zona   

def metode_pembayaran():
    while True:
        print("\n=== METODE PEMBAYARAN ===")
        print("1. Transfer Bank")
        print("2. COD")
        print("3. QRIS")

        pilih = input("Pilih metode (1-3): ")

        if pilih == "1":
            return "Transfer Bank"
        elif pilih == "2":
            return "COD"
        elif pilih == "3":
            return "QRIS"
        else:
            print("Input tidak valid! Pilih angka 1-3.")


def tampilkan_struk(data_pesanan, ongkir, total_akhir, info_kirim, total_berat_paket, metode_pembayaran):
    
    waktu_transaksi = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    biaya_ongkir, harga_kg_ongkir, tujuan_kirim, zona_kirim = info_kirim
    total_produk = 0               
    
    print("\n" + "="*50)
    print("           ✨ STRUK PEMBAYARAN GREENBEAN ✨")
    print("="*50)
    print(f"Waktu Transaksi: {waktu_transaksi}")
    print(f"Metode Bayar    : {metode_pembayaran}")
    print("-" * 50)
    
    print("RINCIAN PESANAN:")
    total_produk = 0
    for item in data_pesanan:
        harga_satuan = item['harga_per_kg']
        harga_total = item['harga_total']

        print(f"  > {item['produk']} ({item['jenis']})")
        print(f"    {item['berat']:.2f} Kg x Rp {harga_satuan:.2f} = Rp {harga_total:.2f}")
        total_produk += item['harga_total'] 
    print("-" * 50)
    
    print("RINCIAN PENGIRIMAN:")
    print(f"  Tujuan: {tujuan_kirim} ({zona_kirim})")
    print(f"  Total Berat: {total_berat_paket:.2f} Kg")
    
    print("\nTOTAL HARGA:")
    print(f"  Total Belanja Produk : Rp {total_produk:.2f}")
    print(f"  Biaya Kirim ({harga_kg_ongkir:.2f}/Kg) : Rp {biaya_ongkir:.2f}")
    print("-" * 50)
    print(f"  TOTAL YANG HARUS DIBAYAR : Rp {total_akhir:.2f}")
    print("="*50)
    print("   TERIMA KASIH TELAH BERBELANJA DI GREENBEAN^^")
    print("="*50 + "\n")



def minta_ulasan():
    print("\n" + "="*50)
    print("   TERIMA KASIH TELAH MENGGUNAKAN JASA KAMI! 🙏")
    print("="*50)
    
    while True:
        ulasan = input("Apakah Anda puas menggunakan aplikasi ini? (Ya/Tidak): ").lower()
        if ulasan == "ya":
            print("Kami senang Anda puas! Silakan kembali berbelanja.")
            
        elif ulasan == "tidak":
            print("Mohon maaf atas ketidaknyamanan Anda. Kami akan terus berusaha meningkatkan layanan kami.")
            
        else:
            print("Input tidak valid. Mohon jawab 'Ya' atau 'Tidak'.")
            break
        input("Tekan Enter untuk kembali ke menu utama")
        break
            


def menu_utama():
    while True:
        header()
        print("=========== MENU UTAMA ===========")
        print("1. Register")
        print("2. Log in")
        print("3. Keluar")
        pilih = input("Masukkan pilihan: ")
        if pilih == "1":
            header()
            username, role = register()
        elif pilih == "2":
            header()
            username, role = login()

        elif pilih == "3":
            print("Terimakaih atas kunjungan anda ^^")
            break
        else:
            print("Masukkan pilihan nomor yang tersedia")
            input("Tekan Enter untuk mencoba lagi")
        if username and role:
            if role.lower() == "admin":
                menu_admin(username)
            elif role.lower() == "penjual":
                menu_penjual(username)
            elif role.lower() == "pembeli":
                menu_pembeli(username)

def menu_admin(username):
    while True:
        header()
        print("\n=== MENU ADMIN ===")
        print("1. Lihat daftar produk edamame")
        print("2. Lihat Laporan Pembelian")
        print("3. Logout")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            header()
            df = pd.read_csv("dataEdamame.csv")
            produk_list = [[row["Nama Toko"],row["Produk"], row["Stok"], f"Rp{row['Harga Lokal']}", f"Rp{row['Harga Ekspor']}"]
            for i, (_, row) in enumerate(df.iterrows())]
            print(tabulate(produk_list, headers=["Nama Toko", "Produk", "Stok", "Harga Lokal", "Harga Ekspor"], tablefmt="fancy_grid"))
        elif pilihan == "2":
            header()
            df = pd.read_csv("riwayatpenjualan.csv")
            print("\n=== LAPORAN PEMBELIAN ===")
            if df.empty:
                print("Belum ada transaksi.")
            produk_list = [[row["Waktu"], row["Pembeli"], row["Toko"], row["Produk"], row["Jenis"], row["Berat"], f"Rp{row['Harga Total']}"
                            , f"Rp{row['Total Bayar']}", row["Pembayaran"]]for i, (_, row) in enumerate(df.iterrows())]
            print(tabulate(produk_list, headers=[ "Waktu","Pembeli","Toko","Produk","Jenis", "Berat", "Harga Total", "Total Bayar", "Pembayaran"], 
                           tablefmt="fancy_grid"))
        elif pilihan == "3":
            print("Logout berhasil!\n")
            return
        else:
            print("Pilihan tidak valid!")
        input("\nTekan ENTER untuk kembali...")


def menu_penjual(username):
    while True:
        header()
        print("\n===== MENU PENJUAL =====")
        print("1. Tambah Produk")
        print("2. Hapus Produk")
        print("3. Lihat Produk")
        print("4. Ubah Data Produk")
        print("5. Lihat Riwayat Penjualan")
        print("6. Lihat Permintaan Pembeli")
        print("7. Keluar")
        pilih = input("Masukkan pilihan: ")
        if pilih == "1":
            tambahProduk(username)
        elif pilih == "2":
            hapusData(username)
        elif pilih == "3":
            lihatProduk(username)
        elif pilih == "4":
            ubahData(username)
        elif pilih == "5":
            lihatRiwayat_Penjualan(username)
        elif pilih == "6":
            lihatPermintaan_Pembeli(username)
        elif pilih == "7":
            print("Keluar dari menu penjual...")
            break
        else:
            print("Masukkan nomor yang tersedia")
        input("\nTekan ENTER untuk kembali...")


def menu_pembeli(username):
    while True:
        header()
        print("\n=== MENU PEMBELI ===")
        print("1. Lihat Produk")
        print("2. Beli Produk")
        print("3. Selesai")        
        pilihan = input("Pilih opsi (1-3): ")
        df = pd.read_csv("dataEdamame.csv")
        if pilihan == "1":
            toko_terpilih = pilih_toko(df)
            os.system('cls')
            toko_produk = lihat_produk_toko(df, toko_terpilih) 
            if not toko_produk.empty:
                input("\nTekan ENTER untuk kembali ke menu pembeli")
            
        elif pilihan == "2":
            toko_terpilih = pilih_toko(df)
            os.system('cls')
            toko_produk = lihat_produk_toko(df, toko_terpilih)
            
            total_harga, total_berat, daftar_pesanan = beliproduk(df, username, toko_terpilih)

            if daftar_pesanan:
                os.system('cls')
                if total_berat > 0:
                    ongkir_data = hitung_ongkir(total_berat)
                    total_akhir = total_harga + ongkir_data[0]

                    pembayaran = metode_pembayaran()

                    simpan_riwayatPenjualan(daftar_pesanan, total_harga, username, daftar_pesanan[0]["toko"], pembayaran)

                    os.system('cls')
                    tampilkan_struk(daftar_pesanan,ongkir_data[0],total_akhir,ongkir_data,total_berat,pembayaran)

            input("\nTekan Enter untuk kembali...")

        elif pilihan == "3":
                minta_ulasan()
                break   
        else:
                print("Masukkan angka 1, 2, atau 3!")
                input("\nTekan ENTER untuk kembali...")

menu_utama()

