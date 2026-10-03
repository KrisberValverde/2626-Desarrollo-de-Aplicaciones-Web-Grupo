from flask_login import UserMixin
from conexion.conexion import obtener_conexion
from psycopg2.extras import RealDictCursor

class Usuario(UserMixin):
    def __init__(self, id_usuario, usuario, password, rol='cliente'):
        self.id = str(id_usuario)
        self.usuario = usuario
        self.password = password
        self.rol = rol

    @staticmethod
    def obtener_por_id(user_id):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id, usuario, password, rol FROM usuarios WHERE id = %s", (int(user_id),))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return Usuario(
                    user_data['id'], 
                    user_data['usuario'], 
                    user_data['password'], 
                    user_data.get('rol', 'cliente')
                )
        except Exception as e:
            print(f"Error en obtener_por_id: {e}")
        return None

    @staticmethod
    def obtener_por_nombre(nombre_usuario):
        if not nombre_usuario:
            return None
            
        nombre_limpio = nombre_usuario.strip()
        try:
            conn = obtener_conexion()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Busqueda insensible a mayusculas/minusculas y limpiezas de espacios en DB
            cursor.execute("SELECT id, usuario, password, rol FROM usuarios WHERE LOWER(TRIM(usuario)) = LOWER(%s)", (nombre_limpio,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return Usuario(
                    user_data['id'], 
                    user_data['usuario'], 
                    user_data['password'], 
                    user_data.get('rol', 'cliente')
                )
        except Exception as e:
            print(f"Error en obtener_por_nombre: {e}")
        return None