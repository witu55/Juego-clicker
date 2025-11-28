from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class ThirdWin(QWidget):
    def __init__(self, clicks, clicks_per_click, cps,
                 price_per_click, price_increment, increment_step,
                 cps_cooldown, callback_volver):
        super().__init__()
        self.setWindowTitle("Tienda")
        self.setGeometry(220, 220, 900, 700)

        # Estado recibido
        self.clicks = clicks
        self.clicks_per_click = clicks_per_click
        self.cps = cps
        self.price_per_click = price_per_click
        self.price_increment = price_increment
        self.increment_step = increment_step
        self.cps_cooldown = cps_cooldown
        self.callback_volver = callback_volver

        # Precios
        self.price_cps = 200
        self.price_cooldown = 400

        # Fondo
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("lightgray"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Encabezado
        label = QLabel("Bienvenido a la Tienda")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(label)

        # Estado actual
        self.clicks_label = QLabel(f"Tienes {self.clicks} clicks")
        self.clicks_label.setAlignment(Qt.AlignCenter)
        self.clicks_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.clicks_label)

        # ---- Mejora: +1 per click ----
        self.per_click_label = QLabel(f"Clicks per click: {self.clicks_per_click}")
        self.per_click_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(self.per_click_label)

        self.btn_per_click = QPushButton("+1 per click")
        self.btn_per_click.setMinimumSize(250, 100)
        self.btn_per_click.setStyleSheet("background-color: lightblue; font-size: 22px;")
        self.btn_per_click.clicked.connect(self.comprar_per_click)
        layout.addWidget(self.btn_per_click)

        self.price_label = QLabel(f"Precio: {self.price_per_click} clicks")
        self.price_label.setStyleSheet("font-size: 20px; color: gray;")
        layout.addWidget(self.price_label)

        # ---- Bloque conjunto: +1 click/s y CPS Cooldown ----
        h_layout_buttons = QHBoxLayout()

        # Botón +1 click/s
        self.btn_cps = QPushButton("+1 click/s")
        self.btn_cps.setMinimumSize(250, 100)
        self.btn_cps.setStyleSheet("background-color: lightblue; font-size: 22px;")
        self.btn_cps.clicked.connect(self.comprar_cps)
        h_layout_buttons.addWidget(self.btn_cps)

        # Botón CPS Cooldown
        self.btn_cooldown = QPushButton("CPS Cooldown")
        self.btn_cooldown.setMinimumSize(250, 100)
        self.btn_cooldown.setStyleSheet("background-color: lightblue; font-size: 22px;")
        self.btn_cooldown.clicked.connect(self.comprar_cooldown)
        h_layout_buttons.addWidget(self.btn_cooldown)

        layout.addLayout(h_layout_buttons)

        # Labels de estado y precios alineados
        h_layout_labels = QHBoxLayout()

        self.cps_label = QLabel(f"Clicks por segundo: {self.cps}")
        self.cps_label.setAlignment(Qt.AlignCenter)
        self.cps_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        h_layout_labels.addWidget(self.cps_label)

        self.cooldown_label = QLabel(f"CPS Cooldown: {self.cps_cooldown:.2f}")
        self.cooldown_label.setAlignment(Qt.AlignCenter)
        self.cooldown_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        h_layout_labels.addWidget(self.cooldown_label)

        layout.addLayout(h_layout_labels)

        h_layout_prices = QHBoxLayout()

        self.price_cps_label = QLabel(f"Precio: {self.price_cps} clicks")
        self.price_cps_label.setAlignment(Qt.AlignCenter)
        self.price_cps_label.setStyleSheet("font-size: 20px; color: gray;")
        h_layout_prices.addWidget(self.price_cps_label)

        self.price_cooldown_label = QLabel(f"Precio: {self.price_cooldown} clicks")
        self.price_cooldown_label.setAlignment(Qt.AlignCenter)
        self.price_cooldown_label.setStyleSheet("font-size: 20px; color: gray;")
        h_layout_prices.addWidget(self.price_cooldown_label)

        layout.addLayout(h_layout_prices)

        # Botón Volver
        h_layout = QHBoxLayout()
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setMinimumSize(200, 80)
        self.btn_volver.setStyleSheet("background-color: lightcoral; font-size: 22px; font-weight: bold;")
        self.btn_volver.clicked.connect(self.volver_a_segunda)
        h_layout.addStretch()
        h_layout.addWidget(self.btn_volver)
        layout.addLayout(h_layout)

        self.setLayout(layout)

    # ---- Lógica de compras ----
    def comprar_per_click(self):
        if self.clicks >= self.price_per_click:
            self.clicks -= self.price_per_click
            self.clicks_per_click += 1
            self.clicks_label.setText(f"Tienes {self.clicks} clicks")
            self.per_click_label.setText(f"Clicks per click: {self.clicks_per_click}")
            self.price_per_click += self.price_increment
            self.price_increment += self.increment_step
            self.price_label.setText(f"Precio: {self.price_per_click} clicks")
        else:
            self.price_label.setText(f"Precio: {self.price_per_click} clicks (No tienes suficientes)")

    def comprar_cps(self):
        if self.clicks >= self.price_cps:
            self.clicks -= self.price_cps
            self.cps += 1
            self.clicks_label.setText(f"Tienes {self.clicks} clicks")
            self.cps_label.setText(f"Clicks por segundo: {self.cps}")
        else:
            self.price_cps_label.setText(f"Precio: {self.price_cps} clicks (No tienes suficientes)")

    def comprar_cooldown(self):
        if self.cps_cooldown <= 0.1:
            self.price_cooldown_label.setText("Nivel Máximo alcanzado")
            return

        if self.clicks >= self.price_cooldown:
            self.clicks -= self.price_cooldown
            self.cps_cooldown -= 0.01
            if self.cps_cooldown < 0.1:
                self.cps_cooldown = 0.1

            self.clicks_label.setText(f"Tienes {self.clicks} clicks")
            self.cooldown_label.setText(f"CPS Cooldown: {self.cps_cooldown:.2f}")

            if self.cps_cooldown <= 0.1:
                self.price_cooldown_label.setText("Nivel Máximo alcanzado")
            else:
                self.price_cooldown_label.setText(f"Precio: {self.price_cooldown} clicks")
        else:
            self.price_cooldown_label.setText(f"Precio: {self.price_cooldown} clicks (No tienes suficientes)")

    def volver_a_segunda(self):
        if self.callback_volver:
            self.callback_volver(
                self.clicks,
                self.clicks_per_click,
                self.cps,
                self.price_per_click,
                self.price_increment,
                self.increment_step,
                self.cps_cooldown
            )
        self.close()

def open_store(clicks, clicks_per_click, cps, price_per_click, price_increment, increment_step, cps_cooldown, callback_volver):
    ventana = ThirdWin(
        clicks, clicks_per_click, cps,
        price_per_click, price_increment, increment_step,
        cps_cooldown, callback_volver
    )
    ventana.show()
    return ventana
