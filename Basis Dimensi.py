from sympy import Matrix

# Matriks koefisien dari sistem homogen
A = Matrix([[2, -1, 3],
            [1,  1, -1]])

# Rank via SymPy
rank = A.rank()

# Basis dan dimensi ruang solusi (nullspace)
nullspace = A.nullspace()
dim = len(nullspace)

# Output
print("Rank:", rank)
print("Dimensi ruang solusi:", dim)
print("Basis ruang solusi:")
for v in nullspace:
    print(v)