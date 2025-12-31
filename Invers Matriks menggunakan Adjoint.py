# ================================
# INVERSE MATRIX 4x4 (COFACTOR)
# TANPA REKURSI
# ================================

# determinan 2x2
def det2(a, b, c, d):
    return a*d - b*c


# determinan 3x3 (Sarrus)
def det3(m):
    return (
       - m[0][0]*m[1][1]*m[2][2]
        + m[0][1]*m[1][2]*m[2][0]
        + m[0][2]*m[1][0]*m[2][1]
        - m[0][2]*m[1][1]*m[2][0]
        - m[0][0]*m[1][2]*m[2][1]
        - m[0][1]*m[1][0]*m[2][2]
    )


# ambil minor 3x3 dari matriks 4x4
def minor4(matrix, row, col):
    minor = []
    for i in range(4):
        if i != row:
            minor_row = []
            for j in range(4):
                if j != col:
                    minor_row.append(matrix[i][j])
            minor.append(minor_row)
    return minor


# determinan 4x4 (Laplace baris 0)
def det4(matrix):
    det = 0
    for j in range(4):
        sign = (-1) ** j
        det += sign * matrix[0][j] * det3(minor4(matrix, 0, j))
    return det


# matriks kofaktor
def cofactor_matrix(matrix):
    cof = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            sign = (-1) ** (i + j)
            cof[i][j] = sign * det3(minor4(matrix, i, j))
    return cof


# transpose
def transpose(m):
    return [[m[j][i] for j in range(4)] for i in range(4)]


# inverse 4x4
def inverse_4x4(matrix):
    d = det4(matrix)
    if d == 0:
        raise ValueError("Determinan = 0, tidak punya invers")

    adj = transpose(cofactor_matrix(matrix))
    inv = [[adj[i][j] / d for j in range(4)] for i in range(4)]
    return inv


# ================================
# INPUT USER
# ================================
print("Masukkan matriks 4x4 (pakai spasi):")
A = []

for i in range(4):
    row = list(map(float, input(f"Baris {i+1}: ").split()))
    if len(row) != 4:
        raise ValueError("Harus 4 angka per baris")
    A.append(row)

print("\nMatriks A:")
for r in A:
    print(r)

try:
    invA = inverse_4x4(A)
    print("\nInvers Matriks:")
    for r in invA:
        print(["{:.2f}".format(x) for x in r])
except ValueError as e:
    print("❌", e)
