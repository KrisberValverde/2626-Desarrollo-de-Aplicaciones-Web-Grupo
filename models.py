from flask_login import UserMixin
from conexion.conexion import obtener_conexion

class Usuario(UserMixin):
    def __init__(self, id_usuario, usuario, password):
        self.id = str(id_usuario)
        self.usuario = usuario
        self.password = password

    @staticmethod
    def obtener_por_id(user_id):
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            return Usuario(user_data['id'], user_data['usuario'], user_data['password'])
        return None

    @staticmethod
    def obtener_por_nombre(nombre_usuario):
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (nombre_usuario,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            return Usuario(user_data['id'], user_data['usuario'], user_data['password'])
        return None