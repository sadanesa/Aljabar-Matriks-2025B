import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import sympy as sp
import datetime

# ----------------- Tema Pastel  -----------------
HEADER_COLOR = "#e8d1ff"   
BG_COLOR = "#fff6ff"       
PANEL_COLOR = "#ffffff"    
BUTTON_COLOR = "#ffd8e8"   
TEXT_COLOR = "#4a4a4a"     
ACCENT = "#c7b8ff"         

# ----------------- Fungsi Parsing -----------------
def parse_vec_str(s):
    s = s.strip()
    if not s:
        return []
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    parts = [p.strip() for p in s.split(",") if p.strip()]
    return parts


def parse_vec_sym(s):
    parts = parse_vec_str(s)
    if not parts:
        return []
    result = []
    for p in parts:
        try:
            result.append(sp.sympify(p))
        except Exception:
            if isinstance(p, str) and p.isidentifier():
                result.append(sp.symbols(p))
            else:
                result.append(sp.sympify(p))
    return result


def join_plain(v):
    return "(" + ", ".join(str(x) for x in v) + ")"

# ----------------- Aturan Ekstraksi -----------------
def extract_add_rules(example):
    # parse left and right
    L, R = example.split("=")
    L = L.strip(); R = R.strip()
    if "+" not in L:
        raise ValueError("Definisi penjumlahan harus berisi tanda '+' di sebelah kiri '='.")
    left_a, left_b = [p.strip() for p in L.split("+", 1)]
    A = parse_vec_sym(left_a)
    B = parse_vec_sym(left_b)
    Rvec = parse_vec_sym(R)
    if not (A and B and Rvec):
        raise ValueError("Gagal mem-parse vektor pada Definisi penjumlahan.")

    # Untuk menghindari simbol yang berbenturan, gunakan simbol unik untuk tiap komponen
    rules = []  # akan berisi tuple (expr, a_pos_sym, b_pos_sym)
    for i, (r, ai, bi) in enumerate(zip(Rvec, A, B)):
        a_pos = sp.symbols(f"__A{i}")
        b_pos = sp.symbols(f"__B{i}")
        # ganti nama ai menjadi a_pos dan bi menjadi b_pos pada hasil
        expr = sp.simplify(r.subs({ai: a_pos, bi: b_pos}))
        rules.append((expr, a_pos, b_pos))
    return rules, A, B


def extract_scalar_rules(example):
    L, R = example.split("=")
    L = L.strip(); R = R.strip()
    if "(" in L and ")" in L:
        inside = L[L.index("("): L.rindex(")") + 1]
        base = parse_vec_sym(inside)
    else:
        raise ValueError("Definisi perkalian skalar harus memuat bentuk ( ... ) di bagian kiri.")
    Rvec = parse_vec_sym(R)
    if not (base and Rvec):
        raise ValueError("Gagal mem-parse vektor pada definisi perkalian skalar.")

    # gunakan simbol posisi untuk komponen basis agar tidak berbenturan
    rules = []  # list of tuples (expr, base_pos_sym)
    for i, (r, bi) in enumerate(zip(Rvec, base)):
        base_pos = sp.symbols(f"__S{i}")
        k_pos = sp.symbols("__K")
        expr = sp.simplify(r.subs({bi: base_pos}))
        # ekspresi di sini diharapkan menggunakan 'k' untuk skalar; 'k' atau gunakan __K
        rules.append((expr, base_pos))
    return rules, base

# ----------------- Operasi -----------------
def add_vec(rules, U, V):
    res = []
    for (rule_expr, a_pos, b_pos), ui, vi in zip(rules, U, V):
        res.append(sp.simplify(rule_expr.subs({a_pos: ui, b_pos: vi})))
    return res


def scal_vec(rules, kk, U):
    res = []
    kk_sym = sp.sympify(kk)
    for (rule_expr, base_pos), ui in zip(rules, U):
        # rule_expr mungkin mengandung symbol 'k' bergantung pada parsing.
        # lakukan substitusi base_pos ke ui lalu substitusi k ke kk_sym 
        expr1 = rule_expr.subs({base_pos: ui})
        # jika ada simbol 'k' di expr1, substitusi ke kk_sym
        ksym = sp.symbols('k')
        if ksym in expr1.free_symbols:
            expr1 = sp.simplify(expr1.subs({ksym: kk_sym}))
        else:
            # jika tidak ada 'k', coba substitusi __K 
            Kpos = sp.symbols('__K')
            if Kpos in expr1.free_symbols:
                expr1 = sp.simplify(expr1.subs({Kpos: kk_sym}))
        res.append(sp.simplify(expr1))
    return res


def eq_vec_sym(V1, V2):
    M = sp.Matrix(V1) - sp.Matrix(V2)
    for e in M:
        if sp.simplify(e) != 0:
            return False
    return True

# ----------------- Cek Aksioma -----------------
def fill_default_vectors(n, u_str, v_str, w_str):
    def make_or_parse(s, prefix):
        parsed = parse_vec_sym(s)
        if parsed:
            return parsed
        else:
            return [sp.symbols(f"{prefix}{i}") for i in range(n)]
    U_sym = make_or_parse(u_str, "u")
    V_sym = make_or_parse(v_str, "v")
    W_sym = make_or_parse(w_str, "w")
    return U_sym, V_sym, W_sym


def check_axioms(add_example, scalar_example, u_str, v_str, w_str, k_str, m_str):
    try:
        add_rules, A_example, B_example = extract_add_rules(add_example)
        scalar_rules, base_example = extract_scalar_rules(scalar_example)
    except Exception as e:
        return (f"Kesalahan membaca contoh aturan: {e}", [False]*10)

    n = len(add_rules)
    if len(base_example) != n:
        return ("Kesalahan: dimensi contoh perkalian skalar tidak cocok dengan contoh penjumlahan.", [False]*10)

    U_sym, V_sym, W_sym = fill_default_vectors(n, u_str, v_str, w_str)
    if not (len(U_sym) == len(V_sym) == len(W_sym) == n):
        return ("Kesalahan: dimensi tidak sesuai antara contoh dan input vektor.", [False]*10)

    k_in = k_str.strip() if k_str and k_str.strip() else "k"
    m_in = m_str.strip() if m_str and m_str.strip() else "m"

    status = [False]*10
    out_lines = []
    out_lines.append("Cek Aksioma Ruang Vektor\n")
    out_lines.append("Dibuat pada: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
    out_lines.append("")

    # Aksioma 1
    out_lines.append("\n 1) Penutupan penjumlahan\n")
    try:
        UV = add_vec(add_rules, U_sym, V_sym)
        out_lines.append(f"   u + v = {join_plain(UV)}\n")
        status[0] = True
    except Exception as e:
        out_lines.append(f"   Gagal menghitung u+v: {e}\n")
        status[0] = False

    # Aksioma 2
    out_lines.append("")
    out_lines.append("\n 2) Komutatif: u + v = v + u")
    try:
        VU = add_vec(add_rules, V_sym, U_sym)
        out_lines.append(f"   u+v = {join_plain(UV)}\n")
        out_lines.append(f"   v+u = {join_plain(VU)}\n")
        status[1] = eq_vec_sym(UV, VU)
    except Exception as e:
        out_lines.append(f"   Gagal mengecek komutatif: {e}\n")
        status[1] = False

    # Aksioma 3
    out_lines.append("")
    out_lines.append("\n 3) Asosiatif: u + (v + w) = (u + v) + w\n")
    try:
        VW = add_vec(add_rules, V_sym, W_sym)
        U_VW = add_vec(add_rules, U_sym, VW)
        UV2 = add_vec(add_rules, U_sym, V_sym)
        UV2_W = add_vec(add_rules, UV2, W_sym)
        out_lines.append(f"   u+(v+w) = {join_plain(U_VW)}\n")
        out_lines.append(f"   (u+v)+w = {join_plain(UV2_W)}\n")
        status[2] = eq_vec_sym(U_VW, UV2_W)
    except Exception as e:
        out_lines.append(f"   Gagal mengecek asosiatif: {e}\n")
        status[2] = False

    # Aksioma 4 
    out_lines.append("")
    out_lines.append("\n 4) Identitas penjumlahan (0 + u = u)\n")
    zero_vec = []
    ident_ok = True
    try:
        for i in range(n):
            rule_expr, a_pos, b_pos = add_rules[i]
            zi = sp.symbols(f"z{i}")
            lhs = sp.simplify(rule_expr.subs({a_pos: zi, b_pos: U_sym[i]}))
            rhs = sp.simplify(U_sym[i])
            expr = sp.simplify(lhs - rhs)

            if zi in expr.free_symbols:
                sols = sp.solve(sp.Eq(expr, 0), zi, dict=True)
                if sols:
                    sol = sols[0][zi]
                    # pastikan solusi tidak bergantung pada komponen u
                    if any(sym in sol.free_symbols for sym in U_sym):
                        ident_ok = False
                        zero_vec.append(None)
                    else:
                        zero_vec.append(sol)
                else:
                    ident_ok = False
                    zero_vec.append(None)
            else:
                if sp.simplify(expr) == 0:
                    zero_vec.append(rhs)
                else:
                    ident_ok = False
                    zero_vec.append(None)
    except Exception as e:
        out_lines.append(f"   Gagal mencari vektor nol: {e}\n")
        ident_ok = False

    if ident_ok:
        out_lines.append(f"   Vektor nol ditemukan: {join_plain(zero_vec)}\n")
    else:
        out_lines.append("   Vektor nol tidak ditemukan atau bergantung pada u.\n")
    status[3] = ident_ok

    # Aksioma 5 (invers) 
    out_lines.append("")
    out_lines.append("\n 5) Invers penjumlahan (u + (-u) = 0)\n")
    neg = []
    inv_ok = True
    try:
        if ident_ok:
            for i in range(n):
                rule_expr, a_pos, b_pos = add_rules[i]
                yi = sp.symbols(f"y{i}")
                lhs = sp.simplify(rule_expr.subs({a_pos: U_sym[i], b_pos: yi}))
                rhs = zero_vec[i]
                expr = sp.simplify(lhs - rhs)

                if yi in expr.free_symbols:
                    sols = sp.solve(sp.Eq(expr, 0), yi, dict=True)
                    if sols:
                        sol = sols[0][yi]
                        neg.append(sol)
                    else:
                        inv_ok = False
                        neg.append(None)
                else:
                    if sp.simplify(expr) == 0:
                        neg.append(rhs)
                    else:
                        inv_ok = False
                        neg.append(None)
        else:
            inv_ok = False
    except Exception as e:
        out_lines.append(f"   Gagal mencari invers: {e}\n")
        inv_ok = False

    if inv_ok:
        out_lines.append(f"   -u = {join_plain(neg)}\n")
    else:
        out_lines.append("   Invers penjumlahan tidak ditemukan untuk semua komponen.\n")
    status[4] = inv_ok

    # Aksioma 6
    out_lines.append("")
    out_lines.append("\n 6) Penutupan perkalian skalar (k * u dalam ruang)\n")
    try:
        KUs = scal_vec(scalar_rules, k_in, U_sym)
        out_lines.append(f"   k*u = {join_plain(KUs)}\n")
        status[5] = True
    except Exception as e:
        out_lines.append(f"   Gagal menghitung k*u: {e}\n")
        status[5] = False

    # Aksioma 7
    out_lines.append("")
    out_lines.append("\n 7) Distributif: k*(u+v) = k*u + k*v\n")
    try:
        UplusV = add_vec(add_rules, U_sym, V_sym)
        left = scal_vec(scalar_rules, k_in, UplusV)
        right = add_vec(add_rules, scal_vec(scalar_rules, k_in, U_sym), scal_vec(scalar_rules, k_in, V_sym))
        out_lines.append(f"   k*(u+v) = {join_plain(left)}\n")
        out_lines.append(f"   k*u + k*v = {join_plain(right)}\n")
        status[6] = eq_vec_sym(left, right)
    except Exception as e:
        out_lines.append(f"   Gagal mengecek distributif (k*(u+v)): {e}\n")
        status[6] = False

    # Aksioma 8
    out_lines.append("")
    out_lines.append("\n 8) Distributif skalar: (k+m)*u = k*u + m*u\n")
    try:
        left = scal_vec(scalar_rules, f"({k_in})+({m_in})", U_sym)
        right = add_vec(add_rules, scal_vec(scalar_rules, k_in, U_sym), scal_vec(scalar_rules, m_in, U_sym))
        out_lines.append(f"   (k+m)*u = {join_plain(left)}\n")
        out_lines.append(f"   k*u + m*u = {join_plain(right)}\n")
        status[7] = eq_vec_sym(left, right)
    except Exception as e:
        out_lines.append(f"   Gagal mengecek distributif skalar: {e}\n")
        status[7] = False

    # Aksioma 9
    out_lines.append("")
    out_lines.append("\n 9) Asosiatif skalar: (k*m)*u = k*(m*u)\n")
    try:
        left = scal_vec(scalar_rules, f"({k_in})*({m_in})", U_sym)
        inner = scal_vec(scalar_rules, m_in, U_sym)
        right = scal_vec(scalar_rules, k_in, inner)
        out_lines.append(f"   (k*m)*u = {join_plain(left)}\n")
        out_lines.append(f"   k*(m*u) = {join_plain(right)}\n")
        status[8] = eq_vec_sym(left, right)
    except Exception as e:
        out_lines.append(f"   Gagal mengecek asosiatif skalar: {e}\n")
        status[8] = False

    # Aksioma 10
    out_lines.append("")
    out_lines.append("\n 10) Identitas skalar: 1 * u = u\n")
    try:
        left = scal_vec(scalar_rules, 1, U_sym)
        out_lines.append(f"   1*u = {join_plain(left)}\n")
        out_lines.append(f"   u    = {join_plain(U_sym)}\n")
        status[9] = eq_vec_sym(left, U_sym)
    except Exception as e:
        out_lines.append(f"   Gagal mengecek 1*u = u: {e}\n")
        status[9] = False

    out_lines.append("")
    out_lines.append("\n \n RINGKASAN:\n")
    for i, ok in enumerate(status, 1):
        out_lines.append(f"  Aksioma {i}: {'✔ Terpenuhi\n' if ok else '✘ Gagal\n'}")

    return ("".join(out_lines), status)

# ----------------- GUI -----------------
class VectorAxiomChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cek Aksioma Ruang Vektor — By Tim Hilbert Aksiom")
        self.geometry("980x640")
        self.configure(bg=BG_COLOR)
        self._make_styles()
        self._create_widgets()
        self._default_label_bg = self.cget("bg")

    def _make_styles(self):
        style = ttk.Style(self)
        for th in ("clam", "vista", "default"):
            try:
                style.theme_use(th)
                break
            except: pass

        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("TLabelframe", background=BG_COLOR)
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("TEntry", fieldbackground=PANEL_COLOR, foreground=TEXT_COLOR)
        style.configure("TButton", background=BUTTON_COLOR, foreground=TEXT_COLOR)
        style.map('TButton', background=[('active', ACCENT)])

    def _create_widgets(self):
        header = ttk.Label(self, text="Cek Aksioma Ruang Vektor", style="Header.TLabel")
        header.pack(pady=(12,6))

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        left = ttk.Frame(frame)
        left.pack(side="left", fill="y", padx=(0,15))

        ttk.Label(left, text="Definisi Penjumlahan:", style="Sub.TLabel").grid(row=0, column=0, sticky="w")
        self.add_example = tk.Text(left, width=40, height=2, bg=PANEL_COLOR, fg=TEXT_COLOR)
        self.add_example.grid(row=1, column=0, pady=4)

        ttk.Label(left, text="Definisi Perkalian Skalar:", style="Sub.TLabel").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.scal_example = tk.Text(left, width=40, height=2, bg=PANEL_COLOR, fg=TEXT_COLOR)
        self.scal_example.grid(row=3, column=0, pady=4)

        vframe = ttk.Frame(left)
        vframe.grid(row=4, column=0, pady=(10,0))

        labels = ["u =", "v =", "w =", "k =", "m ="]
        self.entries = []

        for i, lab in enumerate(labels):
            ttk.Label(vframe, text=lab, background=BG_COLOR, foreground=TEXT_COLOR).grid(row=i, column=0, sticky="e")
            ent = ttk.Entry(vframe, width=28)
            ent.grid(row=i, column=1, padx=5, pady=2)
            self.entries.append(ent)

        btn_frame = ttk.Frame(left)
        btn_frame.grid(row=5, column=0, pady=(15,0))

        ttk.Button(btn_frame, text="Cek Aksioma", command=self.run_checks).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear Output", command=self.clear_output).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Simpan Laporan", command=self.save_report).grid(row=0, column=2, padx=5)

        right = ttk.Frame(frame)
        right.pack(side="right", fill="both", expand=True)

        statusbar = ttk.Frame(right)
        statusbar.pack(fill="x", pady=(0,8))
        self.status_labels = []

        for i in range(10):
            lbl = ttk.Label(statusbar, text=f"{i+1}", width=3, anchor="center", relief="ridge")
            lbl.pack(side="left", padx=3)
            self.status_labels.append(lbl)

        self.output = ScrolledText(right, wrap="word", font=("Courier", 10), bg=PANEL_COLOR, fg=TEXT_COLOR)
        self.output.pack(fill="both", expand=True)

        ttk.Label(self, text="Isi definisi dan vektor sesuai kebutuhan. Kosongkan u/v/w untuk simbol otomatis.", style="Sub.TLabel").pack(pady=6)

    def run_checks(self):
        add_ex = self.add_example.get("1.0", "end").strip()
        scal_ex = self.scal_example.get("1.0", "end").strip()
        vals = [e.get().strip() for e in self.entries]

        if not add_ex or not scal_ex:
            messagebox.showwarning("Input kosong", "Definisi harus diisi.")
            return

        report, status = check_axioms(add_ex, scal_ex, *vals)
        self.output.delete("1.0", "end")
        self.output.insert("1.0", report)

        for i, ok in enumerate(status):
            lbl = self.status_labels[i]
            if ok:
                lbl.config(background="#d4f8d4", foreground="#075a17")
            else:
                lbl.config(background="#ffd6d6", foreground="#8a1a1a")

    def clear_output(self):
        self.output.delete("1.0", "end")
        for lbl in self.status_labels:
            lbl.config(background=self._default_label_bg, foreground="black")

    def save_report(self):
        txt = self.output.get("1.0", "end").strip()
        if not txt:
            messagebox.showinfo("Kosong", "Tidak ada laporan untuk disimpan.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".txt")
        if fn:
            with open(fn, "w", encoding="utf-8") as f:
                f.write(txt)
            messagebox.showinfo("Tersimpan", "Laporan berhasil disimpan.")

if __name__ == "__main__":
    VectorAxiomChecker().mainloop()