import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit,
    QPushButton, QHBoxLayout, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class LatexEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Fórmulas LaTeX")

        # Crear el layout principal
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Editor de LaTeX
        self.latex_input = QTextEdit(self)
        self.latex_input.setPlaceholderText("Escribe tu fórmula en LaTeX aquí...")
        self.latex_input.setFixedHeight(100)  # Altura reducida del editor
        main_layout.addWidget(self.latex_input)

        # Botón para renderizar la fórmula
        render_button = QPushButton("Renderizar Fórmula")
        render_button.clicked.connect(self.render_formula)
        main_layout.addWidget(render_button)

        # Área de visualización de la fórmula renderizada
        self.formula_label = QLabel(self)
        self.formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.formula_label)

        # Etiqueta de errores
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.error_label)

        # Panel de botones para insertar símbolos
        symbols_scroll_area = QScrollArea(self)
        symbols_scroll_area.setWidgetResizable(True)
        symbols_widget = QWidget()
        symbols_layout = QGridLayout()
        symbols_widget.setLayout(symbols_layout)
        symbols_scroll_area.setWidget(symbols_widget)

        # Agregar símbolos al panel de botones
        self.add_symbol_buttons(symbols_layout)
        main_layout.addWidget(symbols_scroll_area)

    def add_symbol_buttons(self, layout):
        # Diccionario de símbolos organizados por categoría
        symbols = {
            "Operaciones básicas": [
                ("Fracción", r"\frac{}{}"), ("Raíz", r"\sqrt{}"), ("Suma", "+"),
                ("Resta", "-"), ("Multiplicación", r"\times"), ("División", r"\div")
            ],
            "Operaciones Matemáticas": [
            ("Raíz cuadrada", r"\sqrt{x}"), ("Raíz enésima", r"\sqrt[n]{x}"),
            ("Potencia", r"x^n"), ("Subíndice", r"x_n"), ("Fracción", r"\frac{a}{b}"),
            ("Suma", r"\sum_{i=1}^n"), ("Producto", r"\prod_{i=1}^n"),
            ("Integral definida", r"\int_{a}^{b}"), ("Integral doble", r"\iint"),
            ("Integral triple", r"\iiint")
            ],
            "Símbolos Químicos": [
            ("H₂O", r"H_2O"), ("CO₂", r"CO_2"), ("O₂", r"O_2"), ("CH₄", r"CH_4"),
            ("Na⁺", r"Na^+"), ("Cl⁻", r"Cl^-"), ("Fe³⁺", r"Fe^{3+}"), ("SO₄²⁻", r"SO_4^{2-}")
            ],
            "Funciones Trigonométricas y Logarítmicas": [
                ("sin", r"\sin"), ("cos", r"\cos"), ("tan", r"\tan"),
                ("log", r"\log"), ("ln", r"\ln"), ("exp", r"\exp")
            ],
            "Letras Griegas": [
                ("α", r"\alpha"), ("β", r"\beta"), ("γ", r"\gamma"),
                ("Δ", r"\Delta"), ("θ", r"\theta"), ("λ", r"\lambda"),
                ("π", r"\pi"), ("σ", r"\sigma"), ("φ", r"\phi"), ("ω", r"\omega")
            ],
            "Relaciones Lógicas": [
                ("∈", r"\in"), ("∉", r"\notin"), ("∪", r"\cup"), ("∩", r"\cap"),
                ("⊆", r"\subseteq"), ("⊂", r"\subset"), ("⊇", r"\supseteq"), ("⊃", r"\supset")
            ],
            "Flechas": [
                ("→", r"\rightarrow"), ("←", r"\leftarrow"), ("↑", r"\uparrow"),
                ("↓", r"\downarrow"), ("⇌", r"\leftrightarrow"),
                ("⇒", r"\Rightarrow"), ("⇔", r"\Leftrightarrow")
            ],
            "Símbolos de Conjuntos": [
                ("ℕ", r"\mathbb{N}"), ("ℤ", r"\mathbb{Z}"), ("ℚ", r"\mathbb{Q}"),
                ("ℝ", r"\mathbb{R}"), ("ℂ", r"\mathbb{C}")
            ],
            "Álgebra Lineal": [
                ("Matriz", r"\begin{matrix} ... \end{matrix}"),
                ("Determinante", r"\begin{vmatrix} ... \end{vmatrix}"),
                ("Vector Columna", r"\begin{bmatrix} ... \end{bmatrix}"),
                ("Vector Fila", r"\begin{pmatrix} ... \end{pmatrix}"),
                ("Norma", r"\|x\|")
            ],
            "Otros Símbolos": [
                ("∞", r"\infty"), ("∂", r"\partial"), ("°", r"^\circ"),
                ("|x|", r"\vert x \vert"), ("Punto", r"\cdot"),
                ("⊥", r"\perp"), ("||", r"\parallel")
            ]
        }

        row = 0
        col = 0
        for category, items in symbols.items():
            # Añadir una etiqueta de categoría
            label = QLabel(f"<b>{category}</b>")
            layout.addWidget(label, row, col, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
            row += 1
            col = 0
            for text, latex_code in items:
                button = QPushButton(text)
                button.clicked.connect(lambda _, code=latex_code: self.insert_symbol(code))
                layout.addWidget(button, row, col)
                col += 1
                if col > 3:  # Máximo 4 botones por fila
                    col = 0
                    row += 1
            row += 1  # Espacio entre categorías

    def insert_symbol(self, symbol):
        """Inserta el símbolo en el editor de LaTeX."""
        cursor = self.latex_input.textCursor()
        cursor.insertText(symbol)

    def render_formula(self):
        """Renderiza la fórmula LaTeX usando pdflatex y ghostscript, y muestra la imagen resultante."""
        latex_code = self.latex_input.toPlainText()

        if latex_code.strip() == "":
            self.formula_label.setText("Por favor, ingresa una fórmula.")
            self.error_label.clear()
            return

        # Definir el contenido del archivo LaTeX
        latex_content = r"""
        \documentclass{standalone}
        \usepackage{amsmath}
        \begin{document}
        $%s$
        \end{document}
        """ % latex_code

        # Crear archivos temporales
        temp_dir = "/tmp"
        tex_path = os.path.join(temp_dir, "formula.tex")
        pdf_path = os.path.join(temp_dir, "formula.pdf")
        png_path = os.path.join(temp_dir, "formula.png")

        # Guardar el contenido en un archivo .tex
        with open(tex_path, "w") as f:
            f.write(latex_content)

        try:
            # Ejecutar pdflatex para generar el PDF
            subprocess.run(["pdflatex", "-output-directory", temp_dir, tex_path], check=True)

            # Usar Ghostscript para convertir el PDF a PNG con una resolución mayor
            subprocess.run([
                "gs", "-sDEVICE=pngalpha", "-o", png_path,
                "-r150", pdf_path  # Cambia "-r144" a "-r300" o un valor mayor para mejor resolución
            ], check=True)

            # Cargar la imagen generada en QLabel
            pixmap = QPixmap(png_path)
            self.formula_label.setPixmap(pixmap)
            self.formula_label.setScaledContents(False)  # Evitar escalado automático
            self.error_label.clear()

        except subprocess.CalledProcessError as e:
            # Mostrar errores si pdflatex o ghostscript fallan
            self.error_label.setText(f"Error en la fórmula: {str(e)}")
            self.formula_label.clear()

        finally:
            # Eliminar archivos temporales
            for file_path in [tex_path, pdf_path, png_path]:
                if os.path.exists(file_path):
                    os.remove(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LatexEditorApp()
    window.show()
    sys.exit(app.exec())
