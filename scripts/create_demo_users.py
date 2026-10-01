from werkzeug.security import generate_password_hash
import psycopg2.extras
from database import get_connection

USUARIOS = [
    ("juan.perez@usat.edu.pe", "CampusGo#2026", "Juan", "Pérez Sánchez", "PASAJERO", "ACTIVO"),
    ("carlos.mendoza@usat.edu.pe", "CampusGo#2026", "Carlos", "Mendoza Ruiz", "CONDUCTOR", "ACTIVO"),
    ("admin@campusgo.pe", "CampusGo#2026", "Administrador", "CampusGo", "ADMINISTRADOR", "ACTIVO")
]

def main():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # 1. UPSERT compatible con PostgreSQL
        sql_usuario = """
            INSERT INTO usuario (
                email, password_hash, nombres, apellidos, rol, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                nombres = EXCLUDED.nombres,
                apellidos = EXCLUDED.apellidos,
                rol = EXCLUDED.rol,
                estado = EXCLUDED.estado
            RETURNING id, rol;
        """

        sql_pasajero = """
            INSERT INTO pasajero (usuario_id)
            VALUES (%s)
            ON CONFLICT (usuario_id) DO NOTHING;
        """

        sql_conductor = """
            INSERT INTO conductor (usuario_id, licencia, calificacion)
            VALUES (%s, %s, %s)
            ON CONFLICT (usuario_id) DO NOTHING;
        """

        for email, password, nombres, apellidos, rol, estado in USUARIOS:
            password_hash = generate_password_hash(password)
            cursor.execute(
                sql_usuario,
                (email, password_hash, nombres, apellidos, rol, estado)
            )
            user_id, user_rol = cursor.fetchone()

            # 2. Poblar la tabla dependiente según el rol
            if user_rol == "PASAJERO":
                cursor.execute(sql_pasajero, (user_id,))
            elif user_rol == "CONDUCTOR":
                # Licencia dummy para el seed de prueba
                cursor.execute(sql_conductor, (user_id, "LIC-TEST-001", 5.0))

        connection.commit()
        print("Usuarios y roles base inicializados correctamente.")
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()