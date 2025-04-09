from PyQt6.QtWidgets import QMessageBox
from utils.supabase_client import authenticate_user
from views.modules.inventario_view import InventarioView


class LoginController:
    def __init__(self, login_view, main_window_class=None):
        """
        :param login_view: Instancia de LoginView
        :param main_window_class: Se puede pasar para mantener compatibilidad, pero no se usará ya que redirigimos a InventarioView.
        """
        self.login_view = login_view
        self.main_window_class = main_window_class  # No se usará en este caso
        # Conectamos la señal del botón con el método handle_login
        self.login_view.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        usuario = self.login_view.email_input.text().strip()
        contrasenia = self.login_view.password_input.text().strip()

        is_valid, user_data = authenticate_user(usuario, contrasenia)
        if is_valid:
            QMessageBox.information(self.login_view, "Login", f"Bienvenido, {usuario}!")
            # Extraemos el rol del usuario
            rol = user_data.get("role") or "vendedor"
            self.inventario_view = InventarioView(user_role=rol)
            self.inventario_view.show()
            self.login_view.close()
        else:
            QMessageBox.warning(
                self.login_view,
                "Error de autenticación",
                "Usuario o contraseña incorrectos. Por favor, intenta nuevamente."
            )
