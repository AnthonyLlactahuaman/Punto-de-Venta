from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - LlactaSoft")
        self.setFixedSize(1200, 750)  # Ajusta el tamaño de la ventana según prefieras
        self.init_ui()

    def init_ui(self):
        # ========== SECCIÓN IZQUIERDA ==========
        # Título "LOGIN"
        login_title_label = QLabel("LOGIN")
        # Ajusta el tamaño de fuente, color, etc.
        font_title = QFont()
        font_title.setPointSize(70)
        font_title.setBold(True)
        login_title_label.setFont(font_title)
        login_title_label.setStyleSheet("color: #FFFFFF;")

        # Etiqueta "Usuario"
        user_label = QLabel("Usuario")
        user_label.setStyleSheet("color: #FFFFFF; font-size: 20px;")

        # Campo de texto para usuario
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(35)
        self.email_input.setStyleSheet("""
            background-color: #D3D3D3;
            color: #000000;
            border: none;
            border-radius: 5px;
            padding: 5px;
        """)
        self.email_input.setPlaceholderText("Ingresa tu usuario")

        # Etiqueta "Contraseña"
        pass_label = QLabel("Contraseña")
        pass_label.setStyleSheet("color: #FFFFFF; font-size: 20px;")

        # Campo de texto para contraseña
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(35)
        self.password_input.setStyleSheet("""
            background-color: #D3D3D3;
            color: #000000;
            border: none;
            border-radius: 5px;
            padding: 5px;
        """)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Ingresa tu contraseña")

        # Botón "Ingresar"
        self.login_button = QPushButton("Ingresar")
        self.login_button.setFixedHeight(35)
        self.login_button.setStyleSheet("""
            background-color: #E74C3C;
            color: #FFFFFF;
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout interno para el formulario de login
        inner_widget = QWidget()
        inner_layout = QVBoxLayout(inner_widget)
        inner_layout.addStretch()  # Espaciador superior para centrar verticalmente
        inner_layout.addWidget(login_title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        inner_layout.addSpacing(20)
        inner_layout.addWidget(user_label)
        inner_layout.addWidget(self.email_input)
        inner_layout.addSpacing(10)
        inner_layout.addWidget(pass_label)
        inner_layout.addWidget(self.password_input)
        inner_layout.addSpacing(20)
        inner_layout.addWidget(self.login_button)
        inner_layout.addStretch()  # Espaciador inferior para centrar verticalmente

        # Se establece un ancho fijo para el widget interno (por ejemplo, 210 px)
        inner_widget.setFixedWidth(400)

        # Layout izquierdo: contendrá al inner_widget centrado horizontalmente
        left_layout = QVBoxLayout()
        left_layout.addStretch()
        left_layout.addWidget(inner_widget, alignment=Qt.AlignmentFlag.AlignHCenter)
        left_layout.addStretch()

        # ========== SECCIÓN DERECHA ==========
        # Logo
        logo_label = QLabel()
        # Reemplaza la ruta con la tuya (o impórtala desde config.py)
        pixmap = QPixmap("assets/images/logo_Login.png")
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedSize(350, 350)  # Ajusta el tamaño según necesites

        # Texto "LlactaSoft" debajo del logo
        llacta_label = QLabel("LlactaSoft")
        llacta_label.setStyleSheet("color: #E74C3C; font-size: 80px; font-weight: bold;")
        llacta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout vertical para la parte derecha
        right_layout = QVBoxLayout()
        right_layout.addStretch()
        right_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        right_layout.addSpacing(10)
        right_layout.addWidget(llacta_label, alignment=Qt.AlignmentFlag.AlignCenter)
        right_layout.addStretch()

        # ========== LAYOUT PRINCIPAL (HORIZONTAL) ==========
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        self.setLayout(main_layout)

        # ========== ESTILO GENERAL DE LA VENTANA ==========
        self.setStyleSheet("""
            QWidget {
                background-color: #2D3E50;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
