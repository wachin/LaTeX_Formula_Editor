import tkinter as tk
from tkinter import messagebox

class MathSymbolsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Math Symbols")
        self.create_symbol_buttons()

    def create_symbol_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x")

        # Define todos los grupos de símbolos y sus propiedades
        symbols = {
            "Símbolos Básicos": [
                ("+", "+", "Suma"),
                ("-", "-", "Resta"),
                ("*", "\\cdot", "Multiplicación"),
                ("/", "/", "División"),
                ("=", "=", "Igualdad"),
                ("≠", "\\neq", "Diferente de"),
                ("<", "<", "Menor que"),
                (">", ">", "Mayor que"),
                ("≤", "\\leq", "Menor o igual"),
                ("≥", "\\geq", "Mayor o igual"),
            ],
            "Operaciones Matemáticas": [
                ("√", "\\sqrt{x}", "Raíz cuadrada"),
                ("n√", "\\sqrt[n]{x}", "Raíz enésima"),
                ("^", "x^n", "Potencia"),
                ("_", "x_n", "Subíndice"),
                ("/", "\\frac{a}{b}", "Fracción"),
                ("Σ", "\\sum_{i=1}^n", "Suma"),
                ("Π", "\\prod_{i=1}^n", "Producto"),
                ("∫", "\\int_{a}^{b}", "Integral definida"),
                ("∬", "\\iint", "Integral doble"),
                ("∭", "\\iiint", "Integral triple"),
            ],
            "Funciones Trigonométricas y Logarítmicas": [
                ("sin", "\\sin", "Seno"),
                ("cos", "\\cos", "Coseno"),
                ("tan", "\\tan", "Tangente"),
                ("log", "\\log", "Logaritmo"),
                ("ln", "\\ln", "Logaritmo natural"),
                ("exp", "\\exp", "Exponencial"),
            ],
            "Letras Griegas": [
                ("α", "\\alpha", "Alfa"),
                ("β", "\\beta", "Beta"),
                ("γ", "\\gamma", "Gamma"),
                ("Δ", "\\Delta", "Delta mayúscula"),
                ("θ", "\\theta", "Theta"),
                ("λ", "\\lambda", "Lambda"),
                ("π", "\\pi", "Pi"),
                ("σ", "\\sigma", "Sigma"),
                ("φ", "\\phi", "Phi"),
                ("ω", "\\omega", "Omega"),
            ],
            "Relaciones Lógicas": [
                ("∈", "\\in", "Pertenece a"),
                ("∉", "\\notin", "No pertenece a"),
                ("∪", "\\cup", "Unión"),
                ("∩", "\\cap", "Intersección"),
                ("⊆", "\\subseteq", "Subconjunto o igual"),
                ("⊂", "\\subset", "Subconjunto propio"),
                ("⊇", "\\supseteq", "Superconjunto o igual"),
                ("⊃", "\\supset", "Superconjunto propio"),
            ],
            "Símbolos de Flechas": [
                ("→", "\\rightarrow", "Flecha derecha"),
                ("←", "\\leftarrow", "Flecha izquierda"),
                ("↑", "\\uparrow", "Flecha arriba"),
                ("↓", "\\downarrow", "Flecha abajo"),
                ("⇌", "\\leftrightarrow", "Flecha doble"),
                ("⇒", "\\Rightarrow", "Implicación"),
                ("⇔", "\\Leftrightarrow", "Equivalencia"),
            ],
            "Símbolos de Conjuntos": [
                ("ℕ", "\\mathbb{N}", "Números naturales"),
                ("ℤ", "\\mathbb{Z}", "Números enteros"),
                ("ℚ", "\\mathbb{Q}", "Números racionales"),
                ("ℝ", "\\mathbb{R}", "Números reales"),
                ("ℂ", "\\mathbb{C}", "Números complejos"),
            ],
            "Símbolos de Álgebra Lineal": [
                ("Matriz", "\\begin{matrix} ... \\end{matrix}", "Matriz sin paréntesis"),
                ("Determinante", "\\begin{vmatrix} ... \\end{vmatrix}", "Determinante"),
                ("Vector columna", "\\begin{bmatrix} ... \\end{bmatrix}", "Matriz entre corchetes"),
                ("Vector fila", "\\begin{pmatrix} ... \\end{pmatrix}", "Matriz entre paréntesis"),
                ("Norma", "\\|x\\|", "Norma de un vector"),
            ],
            "Otros Símbolos Útiles": [
                ("∞", "\\infty", "Infinito"),
                ("∂", "\\partial", "Derivada parcial"),
                ("°", "^\\circ", "Grado"),
                ("|x|", "\\vert x \\vert", "Valor absoluto"),
                (".", "\\cdot", "Punto centrado"),
                ("⊥", "\\perp", "Perpendicular"),
                ("||", "\\parallel", "Paralelo"),
            ],
            "Símbolos de Química": [
                ("→", "\\rightarrow", "Reacción hacia productos"),
                ("⇌", "\\rightleftharpoons", "Equilibrio químico"),
                ("∆H", "\\Delta H", "Cambio de entalpía"),
                ("∆S", "\\Delta S", "Cambio de entropía"),
                ("pH", "pH", "Potencial de hidrógeno"),
                ("mol", "mol", "Unidad de cantidad de sustancia"),
                ("M", "M", "Molaridad"),
                ("ppm", "ppm", "Partes por millón"),
                ("%", "%", "Porcentaje"),
                ("→", "\\xrightarrow{Catalizador}", "Reacción con catalizador"),
            ],
        }

        for group_name, symbol_list in symbols.items():
            group_frame = tk.LabelFrame(button_frame, text=group_name, padx=5, pady=5)
            group_frame.pack(fill="x", pady=5)

            for symbol, latex_code, description in symbol_list:
                btn = tk.Button(group_frame, text=symbol, width=5)
                btn.pack(side="left", padx=2, pady=2)
                btn.bind("<Enter>", lambda e, desc=description: self.show_tooltip(e, desc))
                btn.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx()
        y += event.widget.winfo_rooty()
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

if __name__ == "__main__":
    app = MathSymbolsApp()
    app.mainloop()
