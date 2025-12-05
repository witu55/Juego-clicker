import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap
from second_win import open_win2

class FirstWin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido!")
        self.setGeometry(600, 200, 800, 700)

        # Fondo azul
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("blue"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Botón verde claro
        self.btn = QPushButton("Comenzar juego")
        self.btn.setStyleSheet("background-color: lightgreen; font-size: 16px;")
        self.btn.clicked.connect(self.open_second)

        layout.addWidget(self.btn)
        self.setLayout(layout)

        # Aquí guardaremos la referencia
        self.second = None

    def open_second(self):
        # Abrir segunda ventana y guardar referencia
        self.second = open_win2()
        # Cerrar primera ventana
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FirstWin()
    ventana.show()
    sys.exit(app.exec_())
