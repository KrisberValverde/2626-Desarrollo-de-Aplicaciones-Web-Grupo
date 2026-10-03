import os
import psycopg2

def obtener_conexion():
    try:
        # Pega aquí tu External Database URL de Render
        URL_RENDER = "postgresql://boutique_alison_db_user:Os3hAaj6iBVOYKYjH8nqgXEzBkKxUCRx@dpg-datcef0u01pc73e3df4g-a.oregon-postgres.render.com/boutique_alison_db"
        
        # Intenta obtener la variable del entorno; si no existe, usa la URL de Render
        database_url = os.getenv('DATABASE_URL', URL_RENDER)
        
        conexion = psycopg2.connect(database_url)
        return conexion
    except Exception as e:
        raise Exception(f"Error al conectar con PostgreSQL: {e}")