# models/inventory.py
from utils.supabase_client import supabase


def check_product_exists(codigo: str, marca: str) -> bool:
    """
    Verifica si ya existe un producto en la tabla "Inventario"
    con el mismo Código y Marca.
    Retorna True si existe, False en caso contrario.
    """
    try:
        response = supabase.table("Inventario")\
            .select("*")\
            .eq("Codigo", codigo)\
            .eq("Marca", marca)\
            .execute()
        data = response.data
        return bool(data and len(data) > 0)
    except Exception as e:
        print("Error al verificar la existencia del producto:", e)
        return False


def insert_product(product_data: dict):
    """
    Inserta un nuevo producto en la tabla "Inventario".
    Retorna la respuesta de Supabase o None si ocurre un error.
    """
    try:
        response = supabase.table("Inventario").insert(product_data).execute()
        return response.data
    except Exception as e:
        print("Error al insertar producto:", e)
        return None
