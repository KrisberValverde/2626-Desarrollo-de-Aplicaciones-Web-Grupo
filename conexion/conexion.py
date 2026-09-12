import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='127.0.0.1',  # <--- Cambiado de 'localhost' a '127.0.0.1'
            database='db_proyecto_integrador',
            user='root',
            password='Nayluc101#'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        raise Exception(f"Error detallado de conexión MySQL: {e}")