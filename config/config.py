from dotenv import load_dotenv
import os

# Cargar las variables de entorno definidas en el archivo .env
load_dotenv()

# Variables de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Rutas de recursos
# Asumiendo que el directorio assets está en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_LOGIN_PATH = os.path.join(BASE_DIR, "assets", "images", "logo_Login.png")
ICON_LOGO = os.path.join("assets", "images", "logo_blanco.png")
ICON_TIENDA = os.path.join("assets", "icons", "tienda.png")
ICON_INVENTARIO = os.path.join("assets", "icons", "inventario.png")
ICON_VENTAS = os.path.join("assets", "icons", "ventas.png")
ICON_COMPRAS = os.path.join("assets", "icons", "compras.png")
ICON_SUNAT = os.path.join("assets", "icons", "sunat.png")
ICON_GRAFICOS = os.path.join("assets", "icons", "graficos.png")
# Puedes agregar más variables de configuración si es necesario
