
print("Masukkan elemen matriks 3x3:")
A = []

for i in range(3):
    baris = list(map(int, input(f"Baris ke-{i+1} (pisahkan dengan spasi): ").split()))
    A.append(baris)

positif = (
    A[0][0] * A[1][1] * A[2][2] +
    A[0][1] * A[1][2] * A[2][0] +
    A[0][2] * A[1][0] * A[2][1]
)

negatif = (
    A[0][2] * A[1][1] * A[2][0] +
    A[0][0] * A[1][2] * A[2][1] +
    A[0][1] * A[1][0] * A[2][2]
)

determinan = positif - negatif

print("\nMatriks A:")
for baris in A:
    print(baris)

print("\nTotal diagonal positif :", positif)
print("Total diagonal negatif :", negatif)
print("Determinan matriks A   :", determinan)