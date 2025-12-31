import random

def tambah_vektor(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def kali_skalar(k, v):
    return [k * v[0], k * v[1]]

def inner_product(u, v, rumus_str):

    var_rumus = {
        'x1': u[0], 'y1': u[1],
        'x2': v[0], 'y2': v[1],
        'u': u, 'v': v,
        'abs': abs, 'pow': pow 
    }
    
    allowed_globals = {"__builtins__": None}

    try:
        return eval(rumus_str, allowed_globals, var_rumus)
    except Exception:
        return None

def cek_aksioma():
    print("="*40)
    print("   PROGRAM CEK AKSIOMA RHKD (R2)")
    print("="*40)
    print("Format Variabel:")
    print("  u = (x1, y1)")
    print("  v = (x2, y2)")
    print("Contoh input: x1*x2 + y1*y2")
    print("-" * 40)

    rumus = input("Masukkan rumus <u,v>: ")
    
    def IP(vec_a, vec_b):
        return inner_product(vec_a, vec_b, rumus)

    # Validasi awal rumus
    if IP([1,1], [1,1]) is None:
        print("\n[ERROR] Rumus tidak valid atau syntax salah.")
        print("Gunakan format Python standar (misal: 2*x1*x2).")
        return

    print("\n[Mulai Pengujian...]")

    # 1. Loop Uji Aksioma 1-3 (Simetris, Aditivitas, Homogenitas)
    for i in range(10): 
        u = [random.randint(-10, 10), random.randint(-10, 10)]
        v = [random.randint(-10, 10), random.randint(-10, 10)]
        w = [random.randint(-10, 10), random.randint(-10, 10)]
        k = random.randint(-5, 5)

        # Simetris
        if abs(IP(u, v) - IP(v, u)) > 1e-9:
            print(f"GAGAL AKSIOMA 1 (Simetris) pada iterasi {i+1}")
            return

        # Aditivitas
        kiri = IP(tambah_vektor(u, v), w)
        kanan = IP(u, w) + IP(v, w)
        if abs(kiri - kanan) > 1e-9:
            print(f"GAGAL AKSIOMA 2 (Aditivitas) pada iterasi {i+1}")
            return

        # Homogenitas
        if abs(IP(kali_skalar(k, u), v) - (k * IP(u, v))) > 1e-9:
            print(f"GAGAL AKSIOMA 3 (Homogenitas) pada iterasi {i+1}")
            return

    print("[OK] Aksioma 1, 2, 3 Terpenuhi (Uji Acak 10x).")

    # 2. Uji Aksioma 4 (Positivitas & Definiteness)
    
    # A. Cek Non-negativity (Sampel Banyak)
    for _ in range(50):
        test_u = [random.randint(-10, 10), random.randint(-10, 10)]
        val = IP(test_u, test_u)
        if val < -1e-9:
            print(f"GAGAL AKSIOMA 4: Positivitas (Nilai < 0 pada vektor {test_u})")
            return

    # B. Cek Definiteness (Vektor tak nol tidak boleh menghasilkan 0)
    vectors_check = [[1, 0], [0, 1], [1, 1], [-1, 5]]
    for vec in vectors_check:
        val = IP(vec, vec)
        if abs(val) < 1e-9:
            print(f"GAGAL AKSIOMA 4: Definiteness (Vektor {vec} hasil kali dalamnya 0)")
            return

    # C. Cek Vektor Nol
    if abs(IP([0,0], [0,0])) > 1e-9:
        print("GAGAL: <0,0> tidak bernilai 0")
        return

    print("[OK] Aksioma 4 Terpenuhi.")
    print("-" * 40)
    print("KESIMPULAN: Rumus VALID sebagai Ruang Hasil Kali Dalam.")

if __name__ == "__main__":
    cek_aksioma()