def input_matrix(baris, kolom, nama):
    print(f"\nMasukkan elemen matriks {nama}:")
    matriks = []
    for i in range(baris):
        row = []
        for j in range(kolom):
            row.append(int(input(f"{nama}[{i}][{j}] = ")))
        matriks.append(row)
    return matriks


print(" OPERASI MATRIKS ")
print("1. Penjumlahan")
print("2. Pengurangan")
print("3. Perkalian")

pilihan = int(input("Pilih operasi (1/2/3): "))

if pilihan == 1 or pilihan == 2:
    baris = int(input("Masukkan jumlah baris matriks: "))
    kolom = int(input("Masukkan jumlah kolom matriks: "))

    A = input_matrix(baris, kolom, "A")
    B = input_matrix(baris, kolom, "B")

    hasil = []
    for i in range(baris):
        row = []
        for j in range(kolom):
            if pilihan == 1:
                row.append(A[i][j] + B[i][j])
            else:
                row.append(A[i][j] - B[i][j])
        hasil.append(row)

    if pilihan == 1:
        print("\nHasil penjumlahan matriks:")
    else:
        print("\nHasil pengurangan matriks (A - B):")

    for row in hasil:
        print(row)

elif pilihan == 3:
    baris_A = int(input("Masukkan jumlah baris matriks A: "))
    kolom_A = int(input("Masukkan jumlah kolom matriks A: "))
    baris_B = int(input("Masukkan jumlah baris matriks B: "))
    kolom_B = int(input("Masukkan jumlah kolom matriks B: "))

    if kolom_A != baris_B:
        print("Matriks tidak bisa dikalikan (kolom A ≠ baris B)")
    else:
        A = input_matrix(baris_A, kolom_A, "A")
        B = input_matrix(baris_B, kolom_B, "B")

        hasil = [[0 for _ in range(kolom_B)] for _ in range(baris_A)]

        for i in range(baris_A):
            for j in range(kolom_B):
                for k in range(kolom_A):
                    hasil[i][j] += A[i][k] * B[k][j]

        print("\nHasil perkalian matriks:")
        for row in hasil:
            print(row)

else:
    print("Pilihan tidak valid!")
