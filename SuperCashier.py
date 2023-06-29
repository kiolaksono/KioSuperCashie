import sqlite3
from tabulate import tabulate
from condb import create_connection

conn = create_connection()
cursor = conn.cursor()

class Transaction:
    def __init__(self):

        # digunakan untuk menampung hasil input data dari user
        self.header=[['NAMA PRODUK','JUMLAH PRODUK','HARGA/PRODUK','TOTAL HARGA', 'DISKON', 'HARGA DISKON']]
        self.cart=[]

    def headerMenu(self):
        print("\n=======================================================")
        print("=======================TOKO-SHOP=======================")
        print("=======================================================\n")

    def msg_errors(self):
        print("Mohon memasukkan data dengan benar!")

    def addItem(self):
        """
        Method addItem digunakan oleh user untuk menambahkan data belanja.
        Try-except digunakan untuk melakukan pemeriksaan pada hasil input user apakah sudah sesuai atau belum.
        Ketika user salah input, ValueError akan running dan program akan memulai ulang dengan syntax While.
        """ 
        
        while True:
            try:
                self.headerMenu()
                item_name = str(input('Nama Produk: '))
                if(item_name == ""):
                    self.msg_errors()
                    return self.addItem()

                qty = int(input('Jumlah Produk: '))                
                if(qty <= 0):
                    print("Jumlah produk tidak boleh kurang dari 1!\n")  
                    return self.addItem()

                price = int(input('Harga Produk: '))
                if(price <=0):
                    print("Harga produk tidak boleh kurang dari 1 Rupiah")
                    return self.addItem()                    

                total_price = qty*price
                diskon = total_price*0
                harga_diskon = total_price - diskon
                if(total_price >= 500000):
                    diskon = total_price*0.07
                    harga_diskon = total_price - diskon  
                elif(total_price>=300000):
                    diskon = total_price*0.06
                    harga_diskon = total_price - diskon
                elif(total_price>=200000):
                    diskon = total_price*0.05
                    harga_diskon = total_price - diskon

                
                self.cart.append([item_name, qty, price, total_price, diskon, harga_diskon])

                break
            except ValueError:
                self.msg_errors()
                print("\n")
                return self.addItem()
        return self.confirmation()

    def confirmation(self):
    
        """
        Method confirmation digunakan untuk mengkonfirmasi kepada user apakah user sudah selesai
        berbelanja atau belum. 
        """
    
        konfirmasi = str(input("Anda ingin mengakhiri belanja Anda? (Y/N)"))
        if konfirmasi == "Y" or konfirmasi == "y":
            print("Data berhasil ditambahkan.")
            show = self.checkOrder()
        else:
            if konfirmasi == "N" or konfirmasi == "n":
                result = self.addItem()
                return result
            else:
                print("Mohon memasukkan jawaban dengan benar.")
                return self.confirmation()

    def itemName_update(self):
        i = 0
        keywords = str(input("Silahkan masukkan nama produk yang ingin di ubah :"))
        for i in range(len(self.cart)):
            if(self.cart[i][0] == keywords):
                while True :
                    try:
                        print(f"Nama Produk : {keywords}")
                        item_name = str(input(f'Silahkan memasukkan nama produk yang baru :'))
                        if(item_name == ""):
                            print("Nama produk tidak boleh kosong!\n")
                            return self.itemName_update()
                        self.cart[i][0]=item_name
                        break
                    except ValueError:
                        self.msg_errors()
                        return self.itemName_update()
                print(f"Produk {keywords} berhasil diupdate.")
                return self.checkOrder()
        else:
            print("Nama Produk tidak ditemukan!")
            return self.itemName_update()

    def qty_update(self):
        i = 0
        keywords = str(input("Silahkan masukkan nama produk yang ingin diubah :"))
        for i in range(len(self.cart)):
            if(self.cart[i][0] == keywords):
                while True :
                    try:
                        print(f"Nama Produk : {keywords}")
                        print(f"Jumlah sebelumnya : {self.cart[i][1]}")
                        qty = int(input("Ubah jumlah produk menjadi : "))

                        if(qty == 0):
                            print("\n Jumlah terbaru sebanyak 0 pcs")
                            confirm = str(input("Apakah Anda ingin menghapusnya (Y/N) ?"))
                            if(confirm == "Y" or confirm == "y"):
                                self.cart.pop(i)
                                print(f'{keywords} berhasil dihapus!\n')
                                break
                            else:
                                print("Jumlah produk tidak boleh 0")
                                return self.qty_update()
                        else:
                            if(qty > 0):
                                self.cart[i][1] = qty
                                self.cart[i][3] = qty*self.cart[i][2]
                                self.cart[i][4] = self.cart[i][3]*0
                                self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                
                                if(self.cart[i][3] >= 500000):
                                    self.cart[i][4] = self.cart[i][3]*0.07
                                    self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                elif(self.cart[i][3] >= 300000):
                                    self.cart[i][4] = self.cart[i][3]*0.06
                                    self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                elif(self.cart[i][3] >= 200000):
                                    self.cart[i][4] = self.cart[i][3]*0.05
                                    self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                
                                break
                            else:
                                self.msg_errors()
                                return self.qty_update()
                    except ValueError:
                        self.msg_errors()
                        return self.qty_update()
                print(f"Jumlah {keywords} berhasil diupdate.")
                return self.checkOrder()
        else:
            print("Nama Produk tidak ditemukan!")
            return self.qty_update()

    def price_update(self):
        i = 0
        keywords = str(input("Silahkan masukkan nama produk yang ingin diubah : "))
        for i in range(len(self.cart)):
            if(self.cart[i][0] == keywords) :
                while True :
                    try:
                        print(f"Nama Produk : {keywords}")
                        print(f"Harga sebelumnya : {self.cart[i][2]}")
                        price = int(input("Ubah harga produk menjadi : "))

                        if(price == 0):
                            print("\n Harga terbaru tidak boleh 0 Rupiah\n")
                            return self.price_update()
                        else:
                            if(price > 0):
                                self.cart[i][2] = price
                                self.cart[i][3] = self.cart[i][2]*self.cart[i][1]
                                self.cart[i][4] = self.cart[i][3]*0
                                self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                
                                if(self.cart[i][3] >= 500000):
                                    self.cart[i][4] = self.cart[i][3]*0.07
                                    self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                elif(self.cart[i][3] >= 300000):
                                    self.cart[i][4] = self.cart[i][3]*0.06
                                    self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                elif(self.cart[i][3] >= 200000):
                                    self.cart[i][4] = self.cart[i][3]*0.05
                                    self.cart[i][5] = self.cart[i][3] - self.cart[i][4]
                                break
                            else:
                                self.msg_errors()
                                return self.price_update()
                    except ValueError:
                        self.msg_errors()
                        return self.price_update()
                print(f"Harga {keywords} berhasil diupdate.")
                return self.checkOrder()
        else:
            print("Nama Produk tidak ditemukan!")
            return self.price_update()

    def deleteItem(self):
        i = 0
        keywords = str(input("Silahkan masukkan nama produk yang ingin dihapus : "))

        for i in range(len(self.cart)):
            if (self.cart[i][0] == keywords):
                self.cart.pop(i)
                print(f"{keywords} berhasil dihapus!\n")
                return self.checkOrder()
        else:
            print("Nama Produk tidak ditemukan!\n")
            return self.checkOrder()
        
    def resetItem(self):
        confirm = str(input("Apakah anda yakin (Y/N)? "))
        if(confirm == "Y" or confirm == "y"):
            self.cart.clear()
            print("Keranjang berhasil dikosongkan secara menyeluruh!\n")
            return self.checkOrder()
            
        else:
            if(confirm == "N" or confirm == "n"):
                print("Keranjang berhasil disimpan kembali.")
                return self.checkOrder()
            else:
                print("Mohon masukkan jawaban dengan benar!")
                return self.resetItem()
                

    def checkOrder(self):
        self.headerMenu()
        table = self.header + self.cart
        print(tabulate(table))
        print(f"\n Jumlah Data : {len(self.cart)}")
        print("\n 1. Tambah Keranjang\n 2. Ubah Keranjang\n 3. Delete Keranjang\n 4. Reset Keranjang\n 5. Check Out \n 0. Keluar\n")
        print()
        while True:
            try:
                menu_selected = int(input("Pilih Menu (1/2/3/4/5) : "))
                if(menu_selected <0) | (menu_selected > 5):
                    print("Pilih menu dengan benar!\n")
                else:
                    if(menu_selected == 1):
                        return self.addItem()
                    elif(menu_selected == 2):
                        return self.updateCart()
                    elif(menu_selected == 3):
                        return self.deleteItem()
                    elif(menu_selected == 4):
                        return self.resetItem()
                    elif(menu_selected == 5):
                        return self.totalOrder()
                    elif(menu_selected == 0):
                        break

            except ValueError:
                self.msg_errors()
                return self.checkOrder()

    def updateCart(self):
        print("\n 1. Ubah Nama Produk\n 2. Ubah Jumlah Produk\n 3. Ubah Harga Produk\n 0. Menu Awal\n")
        while True:
            try:
                menu_selected = int(input("Pilih Menu(1/2/3) : "))
                if(menu_selected < 0) | (menu_selected > 3):
                    print("Pilih menu dengan benar!\n")
                else:
                    if(menu_selected == 1):
                        return self.itemName_update()
                    elif(menu_selected == 2):
                        return self.qty_update()
                    elif(menu_selected == 3):
                        return self.price_update()
                    elif(menu_selected == 0):
                        return self.checkOrder()

            except ValueError:
                self.msg_errors()
                return self.updateCart()

    def totalOrder(self):
        
        
        table = self.header + self.cart
        confirm = str(input(f"Apakah Anda ingin melakukan pembayaran? "))
        if(confirm == "Y" or confirm == "y") :
            name = str(input("Masukkan Nama Anda = "))
            print(f"Halo, {name}")

            data = (self.cart)
            sql = ''' INSERT INTO belanja(nama_item, jumlah_item, harga, total_harga, diskon, harga_diskon)
                    values (?,?,?,?,?,?)'''
            cursor.executemany(sql, data)
            conn.commit()
            print("PEMBAYARAN BERHASIL")
            
            conn.close()
        elif (confirm == "N" or confirm == "n") :
            print("Silahkan tambahkan/edit item belanjaan anda kembali.")
            return self.checkOrder()
        else :
            print("Data yang anda input tidak valid!")
         

trnsct_123 = Transaction()
trnsct_123.checkOrder()