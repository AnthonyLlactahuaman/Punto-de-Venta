import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from views.login_view import LoginView
from controllers.login_controller import LoginController


class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data  # Contiene info como rol, correo, id_usuario, etc.
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Aplicación - LlactaSoft")
        self.setGeometry(100, 100, 800, 600)

        # Ejemplo sencillo: mostrar rol en un label
        rol = self.user_data.get("rol", "Sin rol")
        label = QLabel(f"Bienvenido(a). Tu rol es: {rol}", self)
        label.move(50, 50)


def main():
    app = QApplication(sys.argv)

    # Creamos la vista y el controlador de login
    login_view = LoginView()
    login_controller = LoginController(login_view, MainWindow)

    login_view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

