import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from third_win import open_store
from final_win import open_final

def cargar_pixmap_seguro(ruta):
    """
    Carga un QPixmap desde ruta. Si no existe o falla, devuelve un placeholder.
    """
    if ruta and os.path.isfile(ruta):
        pm = QPixmap(ruta)
        if not pm.isNull():
            return pm
    # Placeholder: imagen gris con texto
    img = QImage(300, 200, QImage.Format_RGB32)
    img.fill(QColor(200, 200, 200))
    pm = QPixmap.fromImage(img)
    return pm

class SecondWin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clicker")
        self.setGeometry(600, 200, 800, 700)

        # Estado del juego
        self.click_count = 0
        self.clicks_per_click = 1
        self.cps = 0
        self.cps_cooldown = 1.0
        self.price_cooldown = 400
        self.price_per_click = 200
        self.price_increment = 50
        self.increment_step = 50

        # Fondo
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("lightblue"))
        self.setPalette(palette)

        # Layout principal
        layout = QVBoxLayout()

        # Labels de estadísticas
        self.label_total = QLabel(f"Has hecho {self.click_count} clics")
        self.label_total.setAlignment(Qt.AlignCenter)
        self.label_total.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.label_total)

        self.label_cpp = QLabel(f"Clicks por click: {self.clicks_per_click}")
        self.label_cpp.setAlignment(Qt.AlignCenter)
        self.label_cpp.setStyleSheet("font-size: 22px;")
        layout.addWidget(self.label_cpp)

        self.label_cps = QLabel(f"Clicks por segundo: {self.cps}")
        self.label_cps.setAlignment(Qt.AlignCenter)
        self.label_cps.setStyleSheet("font-size: 22px;")
        layout.addWidget(self.label_cps)

        self.label_cooldown = QLabel(f"CPS Cooldown: {self.cps_cooldown:.2f}")
        self.label_cooldown.setAlignment(Qt.AlignCenter)
        self.label_cooldown.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(self.label_cooldown)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # --- Imagen y botón de click en horizontal ---
        h_layout_click = QHBoxLayout()

        # Rutas absolutas seguras
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_no = os.path.join(ruta_base, "tecla no presionada.png")
        ruta_si = os.path.join(ruta_base, "tecla presionada.png")

        # Imagen de la tecla
        self.label_imagen = QLabel(self)
        self.label_imagen.setAlignment(Qt.AlignCenter)

        self.imagen_original = cargar_pixmap_seguro(ruta_no)
        self.imagen_alternativa = cargar_pixmap_seguro(ruta_si)

        # Mostrar siempre escalado con modo suave si hay pixmap
        self.label_imagen.setPixmap(self.imagen_original.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h_layout_click.addWidget(self.label_imagen, stretch=1)

        # Botón principal de clicks
        self.btn_click = QPushButton("Click")
        self.btn_click.setMinimumSize(250, 120)
        self.btn_click.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.btn_click.clicked.connect(self.incrementar_clicks)
        h_layout_click.addWidget(self.btn_click, stretch=0, alignment=Qt.AlignCenter)

        layout.addLayout(h_layout_click)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # Botón tienda
        self.btn_tienda = QPushButton("Tienda")
        self.btn_tienda.setMinimumSize(200, 80)
        self.btn_tienda.setStyleSheet("background-color: lightgreen; font-size: 22px; font-weight: bold;")
        self.btn_tienda.clicked.connect(self.open_store_window)
        layout.addWidget(self.btn_tienda, alignment=Qt.AlignCenter)

        # Botón final
        self.btn_final = QPushButton("Terminar")
        self.btn_final.setMinimumSize(200, 80)
        self.btn_final.setStyleSheet("background-color: orange; font-size: 22px; font-weight: bold;")
        self.btn_final.clicked.connect(self.open_final_window)
        layout.addWidget(self.btn_final, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Timer para auto-clicks
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_clicks)
        self.timer.start(1000)

    # --- Lógica de clicks ---
    def incrementar_clicks(self):
        self.click_count += self.clicks_per_click
        self.label_total.setText(f"Has hecho {self.click_count} clics")

        # Mostrar tecla presionada
        if not self.imagen_alternativa.isNull():
            self.label_imagen.setPixmap(self.imagen_alternativa.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # En caso extremo de pixmap nulo, mantener placeholder ya cargado
            self.label_imagen.setPixmap(self.imagen_original.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        QTimer.singleShot(200, self.volver_a_original)

    def auto_clicks(self):
        if self.cps > 0:
            self.click_count += self.cps
            self.label_total.setText(f"Has hecho {self.click_count} clics")

    def volver_a_original(self):
        if not self.imagen_original.isNull():
            self.label_imagen.setPixmap(self.imagen_original.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # --- Ventanas extra ---
    def open_store_window(self):
        self.store = open_store(
            self.click_count,
            self.clicks_per_click,
            self.cps,
            self.price_per_click,
            self.price_increment,
            self.increment_step,
            self.cps_cooldown,
            self.volver_de_tienda
        )
        self.close()

    def volver_de_tienda(self, clicks, clicks_per_click, cps, price_per_click, price_increment, increment_step, cps_cooldown):
        self.click_count = clicks
        self.clicks_per_click = clicks_per_click
        self.cps = cps
        self.price_per_click = price_per_click
        self.price_increment = price_increment
        self.increment_step = increment_step
        self.cps_cooldown = cps_cooldown

        self.label_total.setText(f"Has hecho {self.click_count} clics")
        self.label_cpp.setText(f"Clicks por click: {self.clicks_per_click}")
        self.label_cps.setText(f"Clicks por segundo: {self.cps}")
        self.label_cooldown.setText(f"CPS Cooldown: {self.cps_cooldown:.2f}")
        self.show()

    def open_final_window(self):
        self.final = open_final(self.click_count)
        self.close()

def open_win2():
    ventana = SecondWin()
    ventana.show()
    return ventana
