import os
import psycopg2

def obtener_conexion():
    try:
        # Si la app está desplegada en Render, usará DATABASE_URL
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            conexion = psycopg2.connect(database_url)
        else:
            # Conexión local con la base de datos de pgAdmin 4
            conexion = psycopg2.connect(
                host='127.0.0.1',
                database='Boutique_Alison_db',  # El nombre exacto que le diste en pgAdmin
                user='postgres',               # Usuario principal
                password='BA2026',             # Contraseña configurada
                port='5432'
            )
        return conexion
    except Exception as e:
        raise Exception(f"Error al conectar con PostgreSQL: {e}")