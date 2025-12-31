import numpy as np

def gauss_elimination(A, B):
    """
    Menyelesaikan SPL AX = B dengan eliminasi Gauss
    """
    # Gabungkan matriks A dan B menjadi matriks augmented
    n = len(B)
    augmented = np.concatenate((A, B.reshape(n, 1)), axis=1)
    
    print("Matriks Augmented [A|B]:")
    for i in range(n):
        for j in range(n):
            print(f"{augmented[i, j]:6.2f}", end=" ")
        print("|", f"{augmented[i, n]:6.2f}")
    print()
    
    # Eliminasi maju
    print("PROSES ELIMINASI GAUSS:")
    print("-" * 60)
    
    for i in range(n):
        # Normalisasi baris i (membuat diagonal utama = 1)
        if augmented[i, i] != 0:
            divisor = augmented[i, i]
            augmented[i] = augmented[i] / divisor
            print(f"Langkah {i*3 + 1}: Normalisasi R{i+1} = R{i+1} / {divisor:.2f}")
            for row in range(n):
                for col in range(n):
                    print(f"{augmented[row, col]:6.2f}", end=" ")
                print("|", f"{augmented[row, n]:6.2f}")
            print()
        
        # Eliminasi kolom i
        for j in range(n):
            if j != i and augmented[j, i] != 0:
                factor = augmented[j, i]
                augmented[j] = augmented[j] - factor * augmented[i]
                print(f"Langkah {i*3 + 2 + (j if j<i else j-1)}: R{j+1} = R{j+1} - ({factor:.2f})×R{i+1}")
                for row in range(n):
                    for col in range(n):
                        print(f"{augmented[row, col]:6.2f}", end=" ")
                    print("|", f"{augmented[row, n]:6.2f}")
                print()
    
    print("HASIL AKHIR (Matriks Identitas):")
    print("-" * 60)
    for i in range(n):
        for j in range(n):
            print(f"{augmented[i, j]:6.2f}", end=" ")
        print("|", f"{augmented[i, n]:6.2f}")
    print()
    
    # Solusi ada di kolom terakhir
    X = augmented[:, n]
    
    return X

def verify_solution(A, X, B):
    """
    Verifikasi solusi dengan menghitung AX dan membandingkan dengan B
    """
    calculated_B = np.dot(A, X)
    error = np.abs(calculated_B - B)
    
    print("VERIFIKASI SOLUSI:")
    print("=" * 60)
    print(f"Solusi X = {X}")
    print()
    
    print("Perhitungan AX = B:")
    print("-" * 40)
    for i in range(len(B)):
        # Tampilkan persamaan
        equation = ""
        for j in range(len(X)):
            if j > 0:
                if A[i, j] >= 0:
                    equation += " + "
                else:
                    equation += " - "
            else:
                if A[i, j] < 0:
                    equation += "-"
            
            equation += f"{abs(A[i, j]):.1f}×{X[j]:.3f}"
        
        # Tampilkan hasil
        print(f"Persamaan {i+1}: {equation}")
        print(f"            = {calculated_B[i]:.6f}")
        print(f"  Seharusnya: {B[i]:.6f}")
        
        # Tampilkan error
        if error[i] < 1e-10:
            print(f"  ✓ TEPAT (error: {error[i]:.2e})")
        else:
            print(f"  ✗ Error: {error[i]:.2e}")
        print()
    
    print(f"Error maksimum: {max(error):.2e}")
    print(f"Error rata-rata: {np.mean(error):.2e}")
    
    return error

def main():
    print("=" * 40)
    print("CONTOH SPL 3x3 Eliminasi Gauss")
    print("=" * 40)
    print("\nPersamaan:")
    print("1) 2x +  y +  z =  7")
    print("2)  x + 3y + 2z = 13")
    print("3) 3x + 2y + 4z = 21")
    print()
    
    # Matriks koefisien A
    A1 = np.array([[2, 1, 1],
                   [1, 3, 2],
                   [3, 2, 4]], dtype=float)
    
    # Vektor konstanta B
    B1 = np.array([7, 13, 21], dtype=float)
    
    print("\n" + "-" * 60)
    
    # Solusi dengan eliminasi Gauss
    solution1 = gauss_elimination(A1, B1)
    
    # Verifikasi
    error1 = verify_solution(A1, solution1, B1)
    
if __name__ == "__main__":
    main()