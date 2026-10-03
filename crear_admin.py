import psycopg2
from werkzeug.security import generate_password_hash

DATABASE_URL = "postgresql://boutique_alison_db_user:Os3hAaj6iBVOYKYjH8nqgXEzBkKxUCRx@dpg-datcef0u01pc73e3df4g-a.oregon-postgres.render.com/boutique_alison_db"

USUARIO_ADMIN = "admin"
PASSWORD_ADMIN = "admin123"
ROL_ADMIN = "administrador"

def crear_admin():
    # Generar el hash compatible con Flask/Werkzeug
    password_hashed = generate_password_hash(PASSWORD_ADMIN)
    
    try:
        # Conexión a la base de datos de Render
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Insertar o actualizar la contraseña encriptada
        query = """
            INSERT INTO usuarios (usuario, password, rol)
            VALUES (%s, %s, %s)
            ON CONFLICT (usuario) 
            DO UPDATE SET password = EXCLUDED.password, rol = EXCLUDED.rol;
        """
        cur.execute(query, (USUARIO_ADMIN, password_hashed, ROL_ADMIN))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("--------------------------------------------------")
        print(f"¡Usuario '{USUARIO_ADMIN}' actualizado correctamente en Render!")
        print("--------------------------------------------------")
        
    except Exception as e:
        print(f"Error al conectar o actualizar: {e}")

if __name__ == "__main__":
    crear_admin()