"""
Crea o actualiza el usuario administrador en la base de datos.

Uso (PowerShell, dentro de la carpeta del proyecto):
    $env:DATABASE_URL = "postgresql://usuario:clave@host/basedatos"
    python crear_admin.py

La URL se lee de una variable de entorno y la contrasena se pide por
teclado, asi que este archivo no contiene ningun dato secreto y se
puede subir a GitHub sin problema de seguridad.
"""
import os
import getpass
import psycopg2
from werkzeug.security import generate_password_hash

USUARIO_ADMIN = "admin"
ROL_ADMIN = "administrador"


def crear_admin():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Falta la variable de entorno DATABASE_URL.")
        return

    password = getpass.getpass("Contraseña nueva para el admin: ")
    confirmacion = getpass.getpass("Repite la contraseña: ")

    if password != confirmacion:
        print("Las contraseñas no coinciden. No se hizo ningún cambio.")
        return
    if len(password) < 8:
        print("Usa al menos 8 caracteres. No se hizo ningún cambio.")
        return

    # Hash compatible con check_password_hash de Flask/Werkzeug
    password_hashed = generate_password_hash(password)

    conn = None
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO usuarios (usuario, password, rol)
            VALUES (%s, %s, %s)
            ON CONFLICT (usuario)
            DO UPDATE SET password = EXCLUDED.password, rol = EXCLUDED.rol;
            """,
            (USUARIO_ADMIN, password_hashed, ROL_ADMIN),
        )
        conn.commit()
        cur.close()
        print(f"Usuario '{USUARIO_ADMIN}' creado o actualizado correctamente.")
    except Exception as e:
        print(f"Error al conectar o actualizar: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    crear_admin()