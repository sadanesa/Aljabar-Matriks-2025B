# ---------------------------------------------------
# 1. SOAL
# ---------------------------------------------------
print("SOAL:")
print("Apakah vektor (4, -1, -2), (2, -2, 5), dan (-9, -24, -6) saling ortogonal?\n")

# ---------------------------------------------------
# 2. DEFINISI VEKTOR
# ---------------------------------------------------
v1 = (4, -1, -2)
v2 = (2, -2, 5)
v3 = (-9, -24, -6)

print("LANGKAH-LANGKAH PENYELESAIAN:")
print("1. Tentukan ketiga vektornya:")
print(f"   v1 = {v1}")
print(f"   v2 = {v2}")
print(f"   v3 = {v3}\n")

# ---------------------------------------------------
# 3. FUNGSI DOT PRODUCT MANUAL
# ---------------------------------------------------
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

# ---------------------------------------------------
# 4. HITUNG DOT PRODUCT
# ---------------------------------------------------
dot12 = dot(v1, v2)
dot13 = dot(v1, v3)
dot23 = dot(v2, v3)

print("2. Hitung dot product (perkalian titik):")
print(f"   v1 · v2 = (4*2) + (-1 * -2) + (-2 * 5) = {dot12}")
print(f"   v1 · v3 = (4*-9) + (-1 * -24) + (-2 * -6) = {dot13}")
print(f"   v2 · v3 = (2*-9) + (-2 * -24) + (5 * -6) = {dot23}\n")

# ---------------------------------------------------
# 5. ANALISIS ORTOGONALITAS
# ---------------------------------------------------
print("3. Syarat ortogonal:")
print("   Dua vektor ortogonal jika dot product = 0.\n")

print("4. Periksa masing-masing dot product:")
if dot12 == 0:
    print("   ✔ v1 ⟂ v2 (ortogonal)")
else:
    print("   ✘ v1 tidak ortogonal terhadap v2")

if dot13 == 0:
    print("   ✔ v1 ⟂ v3 (ortogonal)")
else:
    print("   ✘ v1 tidak ortogonal terhadap v3")

if dot23 == 0:
    print("   ✔ v2 ⟂ v3 (ortogonal)")
else:
    print("   ✘ v2 tidak ortogonal terhadap v3")

# ---------------------------------------------------
# 6. KESIMPULAN
# ---------------------------------------------------
print("\nKESIMPULAN:")
if dot12 == 0 and dot13 == 0 and dot23 == 0:
    print("   Semua dot product = 0 → Ketiga vektor saling ortogonal.")
else:
    print("   Ada dot product ≠ 0 → Ketiga vektor TIDAK saling ortogonal.")