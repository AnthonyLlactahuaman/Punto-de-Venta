from config.config import SUPABASE_URL, SUPABASE_ANON_KEY
from supabase import create_client, Client

# Se crea el cliente de Supabase usando las variables cargadas desde .env
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def authenticate_user(usuario: str, contrasenia: str):
    """
    Verifica si el 'usuario' y 'contrasenia' coinciden con un registro en la tabla User_roles.
    Retorna (True, data_del_usuario) si las credenciales son válidas, o (False, None) en caso contrario.
    """
    try:
        response = (
            supabase.table("User_roles")
            .select("*")
            .eq("usuario", usuario)
            .eq("contrasenia", contrasenia)
            .execute()
        )

        data = response.data
        if data and len(data) > 0:
            return True, data[0]  # data[0] contiene el registro del usuario
        else:
            return False, None
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return False, None
