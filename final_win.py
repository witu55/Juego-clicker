from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import random
import sys

class FinalWin(QWidget):
    def __init__(self, clicks, callback_volver=None):
        super().__init__()
        self.setWindowTitle("Resultado")
        self.setGeometry(250, 250, 500, 300)

        self.clicks = clicks
        self.callback_volver = callback_volver

        layout = QVBoxLayout()

        # Mostrar tus clicks
        self.clicks_label = QLabel(f"Tus clicks: {self.clicks}")
        self.clicks_label.setAlignment(Qt.AlignCenter)
        self.clicks_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.clicks_label)

        # Número aleatorio
        self.random_number = random.randint(1, 10000)
        self.random_label = QLabel(f"Número aleatorio: {self.random_number}")
        self.random_label.setAlignment(Qt.AlignCenter)
        self.random_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.random_label)

        # Comparación
        if self.clicks > self.random_number:
            resultado = f"Tienes MÁS clicks ({self.clicks}) que el número aleatorio ({self.random_number})"
        elif self.clicks < self.random_number:
            resultado = f"Tienes MENOS clicks ({self.clicks}) que el número aleatorio ({self.random_number})"
        else:
            resultado = f"Tienes EXACTAMENTE lo mismo ({self.clicks}) que el número aleatorio ({self.random_number})"

        self.compare_label = QLabel(resultado)
        self.compare_label.setAlignment(Qt.AlignCenter)
        self.compare_label.setStyleSheet("font-size: 14px; color: darkblue; font-weight: bold;")
        layout.addWidget(self.compare_label)

        # Botón volver (opcional)
        if self.callback_volver:
            self.btn_volver = QPushButton("Volver")
            self.btn_volver.setStyleSheet("background-color: lightcoral; font-size: 14px;")
            self.btn_volver.clicked.connect(self.volver)
            layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        # 🔥 Botón cerrar
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setStyleSheet("background-color: red; color: white; font-size: 14px;")
        self.btn_cerrar.clicked.connect(self.cerrar_app)
        layout.addWidget(self.btn_cerrar, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def volver(self):
        if self.callback_volver:
            self.callback_volver(self.clicks)
        self.close()

    def cerrar_app(self):
        # Cierra toda la aplicación
        sys.exit()

def open_final(clicks, callback_volver=None):
    ventana = FinalWin(clicks, callback_volver)
    ventana.show()
    return ventana
