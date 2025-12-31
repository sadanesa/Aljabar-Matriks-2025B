import tkinter as tk
from tkinter import messagebox

class UltraSlimAlgebra:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Algebra Pro")
        self.root.geometry("480x680")
        self.root.configure(bg="#32AAAA")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self.root,
            text="LINEAR ALGEBRA VISUALIZER",
            font=("Helvetica", 14, "bold"), 
            bg="#F5F5F7"
        ).pack(pady=15)

        container = tk.Frame(self.root, bg="white", padx=15, pady=15)
        container.pack(padx=20, fill="x")

        tk.Label(container, text="Vektor x ∈ ℝ⁴", bg="white").pack(anchor="w")
        v_frame = tk.Frame(container, bg="white")
        v_frame.pack(pady=5)

        self.v_entries = []
        for i in range(4):
            e = tk.Entry(v_frame, width=6, justify="center")
            e.insert(0, "0")
            e.pack(side="left", padx=3)
            self.v_entries.append(e)
        
        tk.Label(container, text="Matriks A (3 × 4)", bg="white").pack(anchor="w", pady=(10,0))
        m_frame = tk.Frame(container, bg="white")
        m_frame.pack()

        self.m_entries = []
        for r in range(3):
            row = []
            for c in range(4):
                e = tk.Entry(m_frame, width=6, justify="center")
                e.insert(0, "0")
                e.grid(row=r, column=c, padx=2, pady=2)
                row.append(e)
            self.m_entries.append(row)

        tk.Button(
            self.root,
            text="HITUNG",
            command=self.calculate,
            bg="#28a745",
            fg="white",
            font=("Helvetica", 12, "bold"),
            height=2
        ).pack(padx=30, fill="x", pady=20)

        self.card_tx = tk.Frame(self.root, bg="white", padx=15, pady=15)
        self.card_tx.pack(padx=20, fill="x", pady=(0, 10))

        tk.Label(
            self.card_tx,
            text="HASIL TRANSFORMASI T(x)",
            bg="white",
            font=("Helvetica", 10, "bold"),
            fg="#007AFF"
        ).pack(anchor="w")

        self.label_tx = tk.Label(
            self.card_tx,
            text="",
            bg="white",
            font=("Courier", 11),
            fg="#007AFF",
            justify="left"
        )
        self.label_tx.pack(anchor="w", pady=(5, 0))


        self.card_shear = tk.Frame(self.root, bg="white", padx=15, pady=15)
        self.card_shear.pack(padx=20, fill="x")

        tk.Label(
            self.card_shear,
            text="SETELAH SHEAR arah y (k = 2)",
            bg="white",
            font=("Helvetica", 10, "bold"),
            fg="#28a745"
        ).pack(anchor="w")

        self.label_shear = tk.Label(
            self.card_shear,
            text="",
            bg="white",
            font=("Courier", 11),
            fg="#28a745",
            justify="left"
        )
        self.label_shear.pack(anchor="w", pady=(5, 0))

    def calculate(self):
        try:
            x = [float(e.get()) for e in self.v_entries]

            A = []
            for row in self.m_entries:
                A.append([float(e.get()) for e in row])

            if len(x) != 4 or len(A) != 3 or len(A[0]) != 4:
                raise ValueError("Dimensi tidak sesuai (A harus 3x4 dan x ∈ R⁴)")

            y = []
            for i in range(3):
                y.append(sum(A[i][j] * x[j] for j in range(4)))

            k = 2
            y_shear = [
                y[0],
                y[1] + k * y[0],
                y[2]
            ]

            self.label_tx.config(
                text=f"({y[0]:.2f}, {y[1]:.2f}, {y[2]:.2f})"
            )

            self.label_shear.config(
                text=f"({y_shear[0]:.2f}, {y_shear[1]:.2f}, {y_shear[2]:.2f})"
            )


        except ValueError as e:
            messagebox.showerror("Error Input", str(e))

        

if __name__ == "__main__":
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    app = UltraSlimAlgebra(root)
    root.mainloop()