# Program KantongAjaib
# Spesifikasi Program (tulis nanti hehe)

# KAMUS

import argparse
import sys
import os
from datetime import datetime
import time

def parseCSV(line):
    res = []
    word = ""
    for char in line:
        if char == ";" or char == "\n":
            res.append(word)
            word = ""
        else:
            word += char
    return res

def parseList(data):
    res = ""
    for i in range(len(data)):
        if i == len(data) - 1:
            res += data[i] + "\n"
        else:
            res += data[i] + ";"
    return res

def readCSV(filename):
    file = open(filename, "r")
    data = []
    library = {}

    for line in file:
        data.append(parseCSV(line))

    keys = data[0]
    data.remove(data[0])

    for i in range(len(keys)):
        library[keys[i]] = []
        for j in range(len(data)):
            library[keys[i]].append(data[j][i])
    
    file.close()
    return library

def writeCSV(filename, val):
    backupData = readCSV(filename)

    file = open(filename, "r")
    keylist = parseCSV(file.readline())
    file.close()

    file = open(filename, "w")
    file.write(parseList(keylist))
    for i in range(len(backupData[keylist[0]])):
        temp = []
        for key in keylist:
            temp.append(backupData[key][i])
        file.write(parseList(temp))
    file.write(parseList(val))
    file.close()

def eraseCSV(filename, index):
    backupData = readCSV(filename)

    file = open(filename, "r")
    keylist = parseCSV(file.readline())
    file.close()

    file = open(filename, "w")
    file.write(parseList(keylist))
    for i in range(len(backupData[keylist[0]])):
        if i == index:
            continue
        else:
            temp = []
            for key in keylist:
                temp.append(backupData[key][i])
            file.write(parseList(temp))
    file.close()

def editCSV(filename, index, value):
    backupData = readCSV(filename)

    file = open(filename, "r")
    keylist = parseCSV(file.readline())
    file.close()

    file = open(filename, "w")
    file.write(parseList(keylist))
    for i in range(len(backupData[keylist[0]])):
        if i == index:
            file.write(parseList(value))
        else:
            temp = []
            for key in keylist:
                temp.append(backupData[key][i])
            file.write(parseList(temp))
    file.close()

def searchLib(library, key, val): # Sori masih sequential
    for i in range(len(library[key])):
        if library[key][i] == val:
            return i
    return -1

def searchArr(arr, val): # Sori masih sequential
    for i in range(len(arr)):
        if arr[i] == val:
            return i
    return -1

def findallLib(library, key, val): # Sori ini juga masih sequential
    res = []
    for i in range(len(library[key])):
        if library[key][i] == val:
            res.append(i)
    return res

def findcategoryLib(library, key, category, val): # Ini juga sequential
    res = []
    if category == "=":
        for i in range(len(library[key])):
            if library[key][i] == val:
                res.append(i)
    elif category == ">":
        for i in range(len(library[key])):
            if library[key][i] > val:
                res.append(i)
    elif category == "<":
        for i in range(len(library[key])):
            if library[key][i] < val:
                res.append(i)
    elif category == ">=":
        for i in range(len(library[key])):
            if library[key][i] >= val:
                res.append(i)
    elif category == "<=":
        for i in range(len(library[key])):
            if library[key][i] <= val:
                res.append(i)
    return res

def newIDGenerator(library): # Kalo mau diupgrade jadi random number generator sabi nih
    oldID = "0" if len(library["id"]) == 0 else library["id"][-1]

    if oldID[0].isdigit():
        return str(int(oldID) + 1)
    else:
        char = oldID[0]
        newID = oldID.replace(char, "")
        return char + str(int(newID) + 1)

def capitalize(name):
    res = ""
    isCapital = True

    for char in name:
        if isCapital:
            res += char.upper()
            isCapital = False
        elif char == " ":
            res += char
            isCapital = True
        else:
            res += char
    
    return res

def validasiTanggal(date):
    dateList = []
    word = ""

    for char in date:
        if char == "/":
            if len(word) != 2:
                return False
            dateList.append(int(word))
            word = ""
        else:
            word += char
    if len(word) != 4:
        return False
    dateList.append(int(word))

    if len(dateList) != 3:
        return False

    if dateList[1] == 1 or dateList[1] == 3 or dateList[1] == 5 or dateList[1] == 7 or dateList[1] == 8 or dateList[1] == 10 or dateList[1] == 12:
        return dateList[0] <= 31
    elif dateList[1] == 4 or dateList[1] == 6 or dateList[1] == 9 or dateList[1] == 11:
        return dateList[0] <= 30
    elif dateList[1] == 2:
        if (dateList[2] % 4 == 0 and dateList[2] % 100 != 0) or dateList[2] % 400 == 0: # Kabisat
            return dateList[0] <= 29
        else:
            return dateList[0] <= 28
    else:
        return False

def notReturned(ID):
    dataBorrow = readCSV("gadget_borrow_history.csv")
    dataReturn = readCSV("gadget_return_history.csv")

    borrowList = [[dataBorrow['id'][index], int(dataBorrow['jumlah'][index])] for index in findallLib(dataBorrow, 'id_peminjam', ID) if dataBorrow['is_returned'][index] == 'False']

    for i in range(len(borrowList)):
        jumlahDikembalikan = 0
        for j in findallLib(dataReturn, 'id_pengembalian', borrowList[i][0]):
            jumlahDikembalikan += int(dataReturn['jumlah'][j])
        borrowList[i][1] -= jumlahDikembalikan

    return borrowList

def lessthanequalTanggal(tanggal1, tanggal2):
    dateList1 = []
    dateList2 = []

    word = ""
    for char in tanggal1:
        if char == "/":
            dateList1.append(int(word))
            word = ""
        else:
            word += char
    dateList1.append(int(word))

    word = ""
    for char in tanggal2:
        if char == "/":
            dateList2.append(int(word))
            word = ""
        else:
            word += char
    dateList2.append(int(word))

    if dateList1[2] == dateList2[2]:
        if dateList1[1] == dateList2[1]:
            return dateList1[0] <= dateList2[0]
        else:
            return dateList1[1] < dateList2[1]
    else:
        return dateList1[2] < dateList2[2]

def swap(library, index1, index2):
    for key in library.keys():
        library[key][index1], library[key][index2] = library[key][index2], library[key][index1]

def partition(library, key, low, high):
    i = low - 1
    pivot = library[key][high]

    for j in range(low, high):
        if lessthanequalTanggal(library[key][j], pivot):
            i += 1
            swap(library, i, j)
    
    swap(library, i + 1, high)
    return i + 1

def quickSort(library, key, low, high):    
    if low < high:
        pi = partition(library, key, low, high)

        quickSort(library, key, low, pi - 1)
        quickSort(library, key, pi + 1, high)

    return library

def sortTanggal(library, key):
    return quickSort(library, key, 0, len(library[key]) - 1)

def inputLoc():
    global mainDir

    if len(sys.argv) == 1:
        print("Tidak ada nama folder yang diberikan!")
        print(f"Usage: {os.path.basename(__file__)} <nama_folder>")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("nama_folder")
    args = parser.parse_args()

    folderList = []
    cwd = mainDir
    for (root, dirs, files) in os.walk(cwd, topdown=True):
        folderList += dirs
    
    if args.nama_folder not in folderList:
        print("Nama folder tidak valid!")
        sys.exit(1)

    cwd += "/" + args.nama_folder
    fileList = []
    for (root, dirs, files) in os.walk(cwd, topdown=True):
        fileList += files
    
    requiredFile = ["user.csv", "gadget.csv", "gadget_return_history.csv", "gadget_borrow_history.csv", "consumable.csv", "consumable_history.csv"]

    requiredFile = [files for files in requiredFile if files not in fileList]
    
    if len(requiredFile) > 0:
        print(f"Folder {args.nama_folder} tidak memiliki file:")
        for files in requiredFile:
            print(files)
        sys.exit(1)

    os.chdir(cwd)

def seed(): #ini seed dari randomizernya
    seed = int(datetime.now().strftime("%f"))
    return seed

def getRateRarity():
    numerator = ((seed() * 741) + 347) % 16000 #ini bagian ngerandomnya
    droprate = (numerator/1000) #ini ngehasilin dropratenya, maks 16% dropratenya --> biar persennya ga lebih dari 100%, jd add item cm bs 5x
    if 0 <= numerator <= 1000: 
        if (numerator % 2) != 0:
            rarity = "S"
        else:
            rarity = "A"
    elif 1001 <= numerator <= 2500:
        if (numerator % 2) != 0:
            rarity = "A"
        else:
            rarity = "B"
    elif 2501 <= numerator <= 8000:
        rarity = "B"
    else:
        rarity = "C"
    return (droprate, rarity)

def getConsumables(s,a,b,c): #ini hardcode buat ngehasilin barang gachanya
    data = readCSV("consumable.csv")
    rate = [s,a,b,c]
    rarity = ['S', 'A', 'B', 'C']
    for char in rarity:
        if searchLib(data, 'rarity', char) == -1:
            if char == 'S':
                rate.remove(s)
            elif char == 'A':
                rate.remove(a)
            elif char == 'B':
                rate.remove(b)
            else:
                rate.remove(c)
    sort = []
    for i in range(len(rate)):
        if rate[i] != 0:
            sort.append(rate[i])
    sort.sort() #BELOM DIGANTI SORTNYA

    indexrarity = seed() % sort[-1]
    if 0 <= indexrarity <= sort[0]:
        if sort[0] == s:
            rank = 'S'
        elif sort[0] == a:
            rank = 'A'
        elif sort[0] == b:
            rank = 'B'
        else:
            rank = 'C'
    for i in range(len(sort)-1):
        if sort[i] < indexrarity <= sort[i+1]:
            if sort[i+1] == s:
                rank = 'S'
            elif sort[i+1] == a:
                rank = 'A'
            elif sort[i+1] == b:
                rank = 'B'
            else:
                rank = 'C'

    indexList = findallLib(data, "rarity", rank)
    index = seed() % (len(indexList))
    item = data['nama'][indexList[index]]
    return (item, rank)

def hashString(password):
    g = ord(password[0]) * len(password)
    x = 0
    for i in range(len(password)):
        x += (ord(password[i])*(g**i))
        x = x % 10 ** 10
    return str(x)

def register():
    global query

    data = readCSV("user.csv")

    while True:
        nama = input("Masukkan nama: ")
        if searchLib(data, "nama", nama) != -1:
            print("Nama telah terpakai! Silahkan coba lagi.")
        elif not all(char.isalpha() or (char == " ") for char in nama):
            print("Nama tidak boleh mengandung angka dan simbol! Silahkan coba lagi.")
            continue
        else:
            break

    while True:
        username = input("Masukkan username: ")
        if searchLib(data, "username", username) != -1:
            print("Username telah diambil! Silahkan coba lagi.")
            continue
        else:
            break

    password = input("Masukkan password: ")
    alamat = input("Masukkan alamat: ")

    newInput = [newIDGenerator(data), username, capitalize(nama), alamat, hashString(password), "user"]
    query.append(("write", "user.csv", newInput))

    print(f"User {username} telah berhasil register ke dalam Kantong Ajaib!")

def login():
    global role
    global loginID

    data = readCSV("user.csv")
    index = -1

    while True:
        username = input("Masukkan username: ")
        index = searchLib(data, "username", username)
        if index == -1:
            print("Username belum terdaftar! Silahkan coba lagi.")
            continue
        else:
            break

    passwordCorrect = data["password"][index]

    while True:
        password = input("Masukkan password: ")
        if hashString(password) != passwordCorrect:
            print("Password salah! Silahkan coba lagi.")
            continue
        else:
            break
    
    role = data["role"][index]
    loginID = data["id"][index]
    print(f"Halo {username}! Selamat Datang di Kantong Ajaib.")

def carirarity():
    data = readCSV("gadget.csv")

    rarity = input("Masukkan rarity: ") # Ceunah pasti valid
    
    indexList = findallLib(data, "rarity", rarity)

    print("Hasil pencarian: \n")

    if len(indexList) == 0:
        print(f"Tidak ditemukan gadget dengan rarity {rarity}.")
    else:
        for index in indexList:
            print(f"Nama: {data['nama'][index]}")
            print(f"Deskripsi: {data['deskripsi'][index]}")
            print(f"Jumlah: {data['jumlah'][index]} buah")
            print(f"Rarity: {data['rarity'][index]}")
            print(f"Tahun Ditemukan: {data['tahun_ditemukan'][index]}\n")

def caritahun():
    data = readCSV("gadget.csv")

    tahun = input("Masukkan tahun: ") # Ceunah pasti valid
    jenisKategori = input("Masukkan kategori: ") # Ceunah pasti valid oge

    indexList = findcategoryLib(data, "tahun_ditemukan", jenisKategori, tahun)

    print("Hasil pencarian: \n")

    if len(indexList) == 0:
        print(f"Tidak ditemukan gadget dengan kategori {jenisKategori} {tahun}.")
    else:
        for index in indexList:
            print(f"Nama: {data['nama'][index]}")
            print(f"Deskripsi: {data['deskripsi'][index]}")
            print(f"Jumlah: {data['jumlah'][index]} buah")
            print(f"Rarity: {data['rarity'][index]}")
            print(f"Tahun Ditemukan: {data['tahun_ditemukan'][index]}\n")

def tambahitem():
    global query

    dataG = readCSV("gadget.csv")
    dataC = readCSV("consumable.csv")

    while True: # Bagian ini rada beda ama spesifikasi soal, kalo mau ganti santuy2 aja
        ID = input("Masukkan ID: ")
        if ID[0] == "G":
            if searchLib(dataG, "id", ID) != -1:
                print("ID sudah terpakai! Silahkan coba lagi.")
                continue
            else:
                break
        elif ID[0] == "C":
            if searchLib(dataC, "id", ID) != -1:
                print("ID sudah terpakai! Silahkan coba lagi.")
                continue
            else:
                break
        else:
            print("ID tidak valid! Silahkan coba lagi.")
            continue
    
    while True: # Yang ini juga
        nama = input("Masukkan nama: ")
        if ID[0] == "G":
            if searchLib(dataG, "nama", nama) != -1:
                print("Nama item sudah terpakai! Silahkan coba lagi.")
                continue
            else:
                break
        else: # Nilai ID[0] cuman bisa G ama C
            if searchLib(dataC, "nama", nama) != -1:
                print("Nama item sudah terpakai! Silahkan coba lagi.")
                continue
            else:
                break

    deskripsi = input("Masukkan deskripsi: ")
    jumlah = input("Masukkan jumlah: ")

    while True: # Sama yang ini juga
        rarity = input("Masukkan rarity: ")
        if rarity != "C" and rarity != "B" and rarity != "A" and rarity != "S":
            print("Rarity item tidak valid! Silahkan coba lagi.")
            continue
        else:
            break

    if ID[0] == "G":
        tahun = input("Masukkan tahun ditemukan: ")
        newInput = [ID, nama, deskripsi, jumlah, rarity, tahun]
        query.append(("write", "gadget.csv", newInput))
    else: # Nilai ID[0] cuman bisa G ama C
        newInput = [ID, nama, deskripsi, jumlah, rarity]
        query.append(("write", "consumable.csv", newInput))

    print(f"{'Gadget' if ID[0] == 'G' else 'Consumable'} {nama} berhasil ditambahkan ke database.")

def hapusitem():
    global query

    dataG = readCSV("gadget.csv")
    dataC = readCSV("consumable.csv")
    index = -1

    while True:
        ID = input("Masukkan ID: ")
        if ID[0] == "G":
            index = searchLib(dataG, "id", ID)
            if index == -1:
                print("Tidak ada gadget dengan ID tersebut! Silahkan coba lagi.")
                continue
            else:
                break
        elif ID[0] == "C":
            index = searchLib(dataC, "id", ID)
            if index == -1:
                print("Tidak ada consumable dengan ID tersebut! Silahkan coba lagi.")
                continue
            else:
                break
        else:
            print("ID tidak valid! Silahkan coba lagi.")
            continue
    
    while True:
        ans = input(f"Apakah anda yakin ingin menghapus {dataG['nama'][index] if ID[0] == 'G' else dataC['nama'][index]} (Y/N)? ")
        
        if ans == "Y" or ans == "y":
            if ID[0] == "G":
                query.append(("erase", "gadget.csv", index))
            else: # Nilai ID[0] cuman bisa G ama C
                query.append(("erase", "consumable.csv", index))
            print(f"{'Gadget' if ID[0] == 'G' else 'Consumable'} {dataG['nama'][index] if ID[0] == 'G' else dataC['nama'][index]} berhasil dihapus dari database.")
            break
        elif ans == "N" or ans == "n":
            print(f"{'Gadget' if ID[0] == 'G' else 'Consumable'} {dataG['nama'][index] if ID[0] == 'G' else dataC['nama'][index]} tidak dihapus dari database.")
            break
        else:
            continue

def ubahjumlah():
    global query

    dataG = readCSV("gadget.csv")
    dataC = readCSV("consumable.csv")
    index = -1

    while True:
        ID = input("Masukkan ID: ")
        if ID[0] == "G":
            index = searchLib(dataG, "id", ID)
            if index == -1:
                print("Tidak ada gadget dengan ID tersebut! Silahkan coba lagi.")
                continue
            else:
                break
        elif ID[0] == "C":
            index = searchLib(dataC, "id", ID)
            if index == -1:
                print("Tidak ada consumable dengan ID tersebut! Silahkan coba lagi.")
                continue
            else:
                break
        else:
            print("ID tidak valid! Silahkan coba lagi.")
            continue

    jumlah = int(input("Masukkan jumlah: ")) # Nanti kubuat validasi bagusnya, untuk skrg gini dulu ya
    
    stok = int(dataG['jumlah'][index] if ID[0] == "G" else dataC['jumlah'][index])

    if jumlah + stok < 0:
        print(f"{abs(jumlah)} {dataG['nama'][index] if ID[0] == 'G' else dataC['nama'][index]} gagal dibuang karena stok kurang. Stok sekarang: {stok} (< {abs(jumlah)}).")
    else:
        if ID[0] == "G":
            newInput = [ID, dataG['nama'][index], dataG['deskripsi'][index], str(stok + jumlah), dataG['rarity'][index], dataG['tahun_ditemukan'][index]]
            query.append(("edit", "gadget.csv", index, newInput))
            print(f"{abs(jumlah)} {dataG['nama'][index]} berhasil {'ditambahkan' if jumlah >= 0 else 'dibuang'} karena stok kurang. Stok sekarang: {jumlah + stok}.")
        else: # Nilai ID[0] cuman bisa G ama C
            newInput = [ID, dataC['nama'][index], dataC['deskripsi'][index], str(stok + jumlah), dataC['rarity'][index]]
            query.append(("edit", "consumable.csv", index, newInput))
            print(f"{abs(jumlah)} {dataC['nama'][index]} berhasil {'ditambahkan' if jumlah >= 0 else 'dibuang'} karena stok kurang. Stok sekarang: {jumlah + stok}.")

def pinjam():
    global loginID
    global query

    data = readCSV("gadget.csv")
    dataBorrow = readCSV("gadget_borrow_history.csv")
    index = -1

    while True:
        ID = input("Masukkan ID: ")
        if ID[0] == "G":
            index = searchLib(data, "id", ID)
            if index == -1:
                print("Tidak ada gadget dengan ID tersebut! Silahkan coba lagi.")
                continue
            else:
                break
        else:
            print("ID tidak valid! Silahkan coba lagi.")
            continue
    
    while True:
        tanggal = input("Masukkan tanggal: ")
        if not validasiTanggal(tanggal):
            print("Tanggal tidak valid! Silahkan coba lagi.")
            continue
        else:
            break
    
    while True:
        jumlah = int(input("Masukkan jumlah: ")) # Ini juga nanti harus ku bagusin validasinya
        if jumlah <= 0:
            print("Jumlah peminjaman tidak valid! Silahkan coba lagi.")
            continue
        else:
            break

    stok = int(data["jumlah"][index])

    if stok - jumlah < 0:
        print(f"Item {data['nama'][index]} (x{jumlah}) tidak berhasil dipinjam karena stok kurang!")
    else:
        newInput = [ID, data['nama'][index], data['deskripsi'][index], str(stok - jumlah), data['rarity'][index], data['tahun_ditemukan'][index]]
        borrowInput = [newIDGenerator(dataBorrow), loginID, ID, tanggal, str(jumlah), str(False)]

        query.append(("edit", "gadget.csv", index, newInput))
        query.append(("write", "gadget_borrow_history.csv", borrowInput))

        print(f"Item {data['nama'][index]} (x{jumlah}) berhasil dipinjam.")

def kembalikan():
    global loginID
    global query

    data = readCSV("gadget.csv")
    dataBorrow = readCSV("gadget_borrow_history.csv")
    dataReturn = readCSV("gadget_return_history.csv")

    itemList = notReturned(loginID)

    for i in range(len(itemList)):
        print(f"{i + 1}. {data['nama'][searchLib(data, 'id', dataBorrow['id_gadget'][searchLib(dataBorrow, 'id', itemList[i][0])])]} (x{itemList[i][1]})")
    
    while True:
        nomorPengembalian = int(input("Masukkan nomor pengembalian: "))
        if nomorPengembalian <= 0 or nomorPengembalian > len(itemList):
            print("Nomor pengembalian tidak valid! Silahkan coba lagi.")
            continue
        else:
            break
    
    while True:
        tanggalPengembalian = input("Masukkan tanggal pengembalian: ")
        if not validasiTanggal(tanggalPengembalian):
            print("Tanggal pengembalian tidak valid! Silahkan coba lagi.")
            continue
        else:
            break
    
    while True:
        jumlahPengembalian = int(input(f"Masukkan jumlah item {data['nama'][searchLib(data, 'id', dataBorrow['id_gadget'][searchLib(dataBorrow, 'id', itemList[i][0])])]} yang akan dikembalikan: "))
        if jumlahPengembalian > itemList[nomorPengembalian - 1][1]:
            print(f"Jumlah pengembalian item {itemList[nomorPengembalian - 1][0]} tidak valid! Silahkan coba lagi.")
            continue
        else:
            break
    
    index = searchLib(data, 'id', dataBorrow['id_gadget'][searchLib(dataBorrow, 'id', itemList[i][0])])
    stok = int(data['jumlah'][index])

    newInput = [data['id'][index], data['nama'][index], data['deskripsi'][index], str(stok + jumlahPengembalian), data['rarity'][index], data['tahun_ditemukan'][index]]
    returnInput = [newIDGenerator(dataReturn), itemList[nomorPengembalian - 1][0], tanggalPengembalian, str(jumlahPengembalian)]

    query.append(("edit", "gadget.csv", index, newInput))
    query.append(("write", "gadget_return_history.csv", returnInput))

    if jumlahPengembalian == itemList[nomorPengembalian - 1][1]:
        borrowIndex = searchLib(dataBorrow, 'id', itemList[i][0])
        borrowInput = [dataBorrow['id'][borrowIndex], loginID, dataBorrow['id_gadget'][borrowIndex], dataBorrow['tanggal_peminjaman'][borrowIndex], dataBorrow['jumlah'][borrowIndex], str(True)]

        query.append(("edit", "gadget_borrow_history.csv", borrowIndex, borrowInput))

    print(f"Item {data['nama'][searchLib(data, 'id', dataBorrow['id_gadget'][searchLib(dataBorrow, 'id', itemList[i][0])])]} (x{jumlahPengembalian}) telah dikembalikan.")

def minta():
    global loginID
    global query

    data = readCSV("consumable.csv")
    dataHist = readCSV("consumable_history.csv")
    index = -1

    while True:
        ID = input("Masukkan ID: ")
        index = searchLib(data, "id", ID)
        if index == -1:
            print("Tidak ada consumable dengan ID tersebut! Silahkan coba lagi.")
            continue
        else:
            break
    
    while True: # Sama ini juga nanti harus ku bagusin validasinya
        jumlahPermintaan = int(input("Masukkan jumlah: "))
        if jumlahPermintaan <= 0:
            print("Jumlah permintaan tidak valid! Silahkan coba lagi.")
            continue
        else:
            break
    
    while True:
        tanggalPermintaan = input("Masukkan tanggal permintaan: ")
        if not validasiTanggal(tanggalPermintaan):
            print("Tanggal permintaan tidak valid! Silahkan coba lagi.")
            continue
        else:
            break

    stok = int(data['jumlah'][index])

    if stok - jumlahPermintaan < 0:
        print(f"Item {data['nama'][index]} (x{jumlahPermintaan}) tidak berhasil diambil karena stok kurang!")
    else:
        newInput = [ID, data['nama'][index], data['deskripsi'][index], str(stok - jumlahPermintaan), data['rarity'][index]]
        histInput = [newIDGenerator(dataHist), loginID, ID, tanggalPermintaan, str(jumlahPermintaan)]

        query.append(("edit", "consumable.csv", index, newInput))
        query.append(("write", "consumable_history.csv", histInput))

        print(f"Item {data['nama'][index]} (x{jumlahPermintaan}) telah berhasil diambil!")

def riwayatpinjam():
    dataItem = readCSV("gadget.csv")
    dataUser = readCSV("user.csv")
    dataBorrow = readCSV("gadget_borrow_history.csv")

    display = sortTanggal(dataBorrow, "tanggal_peminjaman")

    for i in range(len(display["id"]) - 1, -1, -1):
        if (len(display["id"]) - 1 - i) % 5 == 0 and i != len(display["id"]) - 1:
            isEnding = True
            while True:
                ans = input("Tampilkan entri berikutnya? (y/n) ")
                if ans == "y" or ans == "Y":
                    isEnding = False
                    break
                elif ans == "n" or ans == "N":
                    break
                else:
                    continue
            if isEnding:
                break
        for key in display.keys():
            if key == "id":
                print(f"ID peminjaman: {display[key][i]}")
            elif key == "id_peminjam":
                namaPeminjam = dataUser['nama'][searchLib(dataUser, "id", display[key][i])]
                print(f"Nama peminjam: {namaPeminjam}")
            elif key == "id_gadget":
                namaItem = dataItem['nama'][searchLib(dataItem, "id", display[key][i])]
                print(f"Nama gadget: {namaItem}")
            elif key == "tanggal_peminjaman":
                print(f"Tanggal peminjaman: {display[key][i]}")
            elif key == "jumlah":
                print(f"Jumlah: {display[key][i]}")
            elif key == "is_returned":
                print(f"Status pengembalian : {'Sudah dikembalikan' if display[key][i] == 'True' else 'Belum dikembalikan'}")
            else:
                continue

def riwayatkembali():
    dataItem = readCSV("gadget.csv")
    dataUser = readCSV("user.csv")
    dataBorrow = readCSV("gadget_borrow_history.csv")
    dataReturn = readCSV("gadget_return_history.csv")

    display = sortTanggal(dataReturn, "tanggal_pengembalian")

    for i in range(len(display["id"]) - 1, -1, -1):
        if (len(display["id"]) - 1 - i) % 5 == 0 and i != len(display["id"]) - 1:
            isEnding = True
            while True:
                ans = input("Tampilkan entri berikutnya? (y/n) ")
                if ans == "y" or ans == "Y":
                    isEnding = False
                    break
                elif ans == "n" or ans == "N":
                    break
                else:
                    continue
            if isEnding:
                break
        for key in display.keys():
            if key == "id":
                print(f"ID pengembalian: {display[key][i]}")
            elif key == "id_pengembalian":
                namaPengembali = dataUser['nama'][searchLib(dataUser, "id", dataBorrow['id_peminjam'][searchLib(dataBorrow, "id", display[key][i])])]
                print(f"Nama pengembali: {namaPengembali}")
                namaItem = dataItem['nama'][searchLib(dataItem, "id", dataBorrow['id_gadget'][searchLib(dataBorrow, "id", display[key][i])])]
                print(f"Nama gadget: {namaItem}")
            elif key == "tanggal_pengembalian":
                print(f"Tanggal pengembalian: {display[key][i]}")
            elif key == "jumlah":
                print(f"Jumlah: {display[key][i]}")
            else:
                continue

def riwayatambil():
    dataConsumable = readCSV("consumable.csv")
    dataUser = readCSV("user.csv")
    dataAmbil = readCSV("consumable_history.csv")

    display = sortTanggal(dataAmbil, "tanggal_pengambilan")

    for i in range(len(display["id"]) - 1, -1, -1):
        if (len(display["id"]) - 1 - i) % 5 == 0 and i != len(display["id"]) - 1:
            isEnding = True
            while True:
                ans = input("Tampilkan entri berikutnya? (y/n) ")
                if ans == "y" or ans == "Y":
                    isEnding = False
                    break
                elif ans == "n" or ans == "N":
                    break
                else:
                    continue
            if isEnding:
                break
        for key in display.keys():
            if key == "id":
                print(f"ID pengambilan: {display[key][i]}")
            elif key == "id_pengambil":
                namaPengambil = dataUser['nama'][searchLib(dataUser, "id", display[key][i])]
                print(f"Nama pengambil: {namaPengambil}")
            elif key == "id_consumable":
                namaConsumable = dataConsumable['nama'][searchLib(dataConsumable, "id", display[key][i])]
                print(f"Nama consumable: {namaConsumable}")
            elif key == "tanggal_pengambilan":
                print(f"Tanggal pengambilan: {display[key][i]}")
            elif key == "jumlah":
                print(f"Jumlah: {display[key][i]}")
            else:
                continue

def save():
    global query

    saveLoc = input("Masukkan nama folder penyimpanan: ")

    folderList = []
    cwd = mainDir

    for (root, dirs, files) in os.walk(cwd, topdown=True):
        folderList += dirs

    cwd += "/" + saveLoc
    if saveLoc not in folderList:
        os.makedirs(cwd)

    fileList = []
    for (root, dirs, files) in os.walk(cwd, topdown=True):
        fileList += files

    os.chdir(cwd)

    if "user.csv" not in fileList:
        file = open("user.csv", "w")
        file.write("id;username;nama;alamat;password;role\n")
        file.close()
    if "gadget.csv" not in fileList:
        file = open("gadget.csv", "w")
        file.write("id;nama;deskripsi;jumlah;rarity;tahun_ditemukan\n")
        file.close()
    if "gadget_return_history.csv" not in fileList:
        file = open("gadget_return_history.csv", "w")
        file.write("id;id_pengembalian;tanggal_pengembalian;jumlah\n")
        file.close()
    if "gadget_borrow_history.csv" not in fileList:
        file = open("gadget_borrow_history.csv", "w")
        file.write("id;id_peminjam;id_gadget;tanggal_peminjaman;jumlah;is_returned\n")
        file.close()
    if "consumable.csv" not in fileList:
        file = open("consumable.csv", "w")
        file.write("id;nama;deskripsi;jumlah;rarity\n")
        file.close()
    if "consumable_history.csv" not in fileList:
        file = open("consumable_history.csv", "w")
        file.write("id;id_pengambil;id_consumable;tanggal_pengambilan;jumlah\n")
        file.close()

    for action in query:
        if action[0] == "write":
            writeCSV(action[1], action[2])
        elif action[0] == "erase":
            eraseCSV(action[1], action[2])
        elif action[0] == "edit":
            editCSV(action[1], action[2], action[3])
        else:
            continue

    inputLoc()
    
    query.clear()

def guide():
    global role

    if role == "admin":
        print("register - untuk melakukan registrasi")
        print("login - untuk melakukan login ke dalam sistem")
        print("carirarity - untuk mencari gadget berdasarkan rarity")
        print("caritahun - untuk mencari gadget berdasarkan tahun ditemukan")
        print("tambahitem - untuk melakukan penambahan item")
        print("hapusitem - untuk melalukan pengurangan item")
        print("riwayatpinjam - untuk melihat riwayat pinjam gadget")
        print("riwayatkembali - untuk melihat riwayat kembali gadget")
        print("riwayatambil - untuk melihat riwayat ambil consumable")
        print("save - untuk melakukan save data")
        print("exit - untuk melakukan exit program")
    elif role == "user":
        print("login - untuk melakukan login ke dalam sistem")
        print("carirarity - untuk mencari gadget berdasarkan rarity")
        print("caritahun - untuk mencari gadget berdasarkan tahun ditemukan")
        print("pinjam - untuk melakukan peminjaman gadget")
        print("kembalikan - untuk melakukan pengembalian gadget")
        print("minta - untuk melakukan permintaan consumable")
        print("save - untuk melakukan save data")
        print("exit - untuk melakukan exit program")
    else: # role == ""
        print("login - untuk melakukan login ke dalam sistem")
        print("save - untuk melakukan save data")
        print("exit - untuk melakukan exit program")

def close():
    while True:
        ans = input("Apakah Anda mau melakukan penyimpanan file yang sudah diubah? (y/n) ")
        if ans == "y" or ans == "Y":
            save()
            break
        elif ans == "n" or ans == "N":
            break
        else:
            continue

def gacha(): #ini fungsi gachanya, mencakup dari awal add item sampe dapet item + ngeremove item yg ditambahin ke gacha + nambahin hasil gacha
    global query

    data = readCSV("consumable.csv")

    itemTaken = [0 for i in range(len(data['nama']))] # Ini kinan ganti

    (chanceS, chanceA, chanceB, chanceC) = (0, 0, 0, 0)
    maks = 1

    while (maks < 6): #biar cuma bisa maks nambahin barang 5 kali in one gacha jd choose wisely
        cons = None
        jml = None

        print(f"\nTambahkan Item untuk Meningkatkan Chance Rarity yang didapat! (Attempt {maks}/5)")
        print("=== INVENTORY ===")
        for i in range(len(data['nama'])):
            print(f"{i + 1}. {data['nama'][i]} (x{int(data['jumlah'][i]) - itemTaken[i]})")
        while (cons == None):
            cons = int(input("Pilih consumable yang mau digunakan: "))
            if 1 <= cons <= (len(data) + 1): #BENER GA YA ... aku kira indeks = banyak data = banyak consumable
                break
            else:
                print("Item tidak ada di inventory!")
                cons = None
        index = cons - 1
        tot = int(data['jumlah'][index]) - itemTaken[index] # Ini kinan ganti
        
        if tot == 0:
            print(f"Barang {data['nama'][index]} sudah habis! Silahkan coba lagi.")
            continue

        while (jml == None):
            jml = int(input("Jumlah yang ingin digunakan: "))
            
            if jml <= 0 or jml > tot:
                print(f"Jumlah tidak valid! Hanya terdapat (x{tot}) {data['nama'][index]} di inventory!")
                jml = None
            else:
                break
        
        itemTaken[index] += jml # Ini kinan ganti
        newInput = [data['id'][index], data['nama'][index], data['deskripsi'][index], str(tot - jml), data['rarity'][index]]
        query.append(("edit", "consumable.csv", index, newInput)) # Ini kinan ganti
        # editCSV("consumable.csv", index, newInput)
        print(f"\n{data['nama'][index]} (x{jml}) berhasil ditambahkan!")
        (droprate, rarity) = getRateRarity()
        print(f"Chance mendapatkan Rarity {rarity} (+{droprate}%)")
        if rarity == 'S':
            chanceS += droprate
        elif rarity == 'A':
            chanceA += droprate
        elif rarity == 'B':
            chanceB += droprate
        else:
            chanceC += droprate
        if maks == 5:
            break
        else:
            while True:
                add = input("\nTambahkan item lagi? (y/n): ")
                if add == 'n' or add == 'N' or add == 'y' or add == 'Y':
                    break
                else:
                    continue
                
            if add == 'n' or add == 'N':
                break
            elif add == 'y' or add == 'Y':
                maks += 1
                continue

    print("Rolling...")
    time.sleep(3.0)
    print("Still rolling...")
    time.sleep(3.0)
    print("Wah, dapet apanih!?!")
    time.sleep(2.0)
    (consumable, rank) = getConsumables(chanceS, chanceA, chanceB, chanceC)  # disini udah ngeadd ke consumable.csv
    print(f"Selamat, Anda mendapatkan {consumable} (x1) Rarity {rank}!")
    
    newIndex= searchLib(data, "nama", consumable)
    newInput = [data['id'][newIndex], consumable, data['deskripsi'][newIndex], str((int(data['jumlah'][newIndex]) - itemTaken[newIndex] + 1)), data['rarity'][newIndex]]
    query.append(("edit", "consumable.csv", newIndex, newInput))

# ALGORITMA PROGRAM UTAMA
if __name__ == "__main__":
    mainDir = os.getcwd()
    inputLoc()

    print("Selamat Datang di Kantong Ajaib!")
    print("Yuk, login terlebih dahulu!\n")
    role = ""
    loginID = ""
    query = []
    login()
    
    while True:
        print("\n==== MENU UTAMA ====\nKetikkan perintah untuk lanjut ke menu berikutnya\n(Untuk bantuan ketik 'help')")
        command = input("\nMasukkan perintah: ")

        if command == "register" and role == "admin": # Hanya admin yang dapat register
            register()

        elif command == "carirarity" and (role == "user" or role == "admin"): # Admin dan user dapat carirarity
            carirarity()

        elif command == "caritahun" and (role == "user" or role == "admin"): # Admin dan user dapat caritahun
            caritahun()
            
        elif command == "tambahitem" and role == "admin": # Hanya admin yang dapat tambahitem
            tambahitem()

        elif command == "hapusitem" and role == "admin": # Hanya admin yang dapat hapusitem
            hapusitem()
        
        elif command == "ubahjumlah" and role == "admin": # Hanya admin yang dapat ubahjumlah
            ubahjumlah()
        
        elif command == "pinjam" and role == "user": # Hanya user yang dapat pinjam
            pinjam()
        
        elif command == "kembalikan" and role == "user": # Hanya user yang dapat kembalikan
            kembalikan()

        elif command == "minta" and role == "user": # Hanya user yang bisa minta
            minta()
        
        elif command == "riwayatpinjam" and role == "admin": # Hanya admin yang bisa riwayatpinjam
            riwayatpinjam()

        elif command == "riwayatkembali" and role == "admin": # Hanya admin yang bisa riwayatkembali
            riwayatkembali()

        elif command == "riwayatambil" and role == "admin": # Hanya admin yang bisa riwayatambil
            riwayatambil()

        elif command == "save" and (role == "admin" or role == "user"): # Admin dan user dapat save
            save()
            print("Progress saved!")

        elif command == "help": # Semua orang dapat help
            guide()

        elif command == "exit": # Semua orang dapat exit
            close()
            print("Sampai jumpa lagi di Kantong Ajaib!")
            break

        elif command == "gacha" and role == "user": # Hanya user yang bisa gacha
            gacha()

        else:
            print("Masukkan perintah tidak valid! Silahkan coba lagi.")
