import pymysql
from app.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
from contextlib import contextmanager

# Función para obtener una conexión a MySQL
def get_mysql_connection():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    return connection

# Context manager para manejar conexiones automáticamente
@contextmanager
def mysql_connection():
    connection = get_mysql_connection()
    try:
        yield connection
    finally:
        connection.close()

# Función para inicializar la estructura de la base de datos
def initialize_database():
    with mysql_connection() as connection:
        try:
            with connection.cursor() as cursor:
                # Crear tabla de casos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS casos (
                        id_caso INT AUTO_INCREMENT PRIMARY KEY,
                        fecha_contacto DATETIME NOT NULL,
                        canal_contacto VARCHAR(50) NOT NULL,
                        PNR VARCHAR(10),
                        tipo_caso VARCHAR(50),
                        comentarios_agente TEXT
                    );
                """)

                # Crear tabla de canales
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS canales (
                        id_canal INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_canal VARCHAR(50) UNIQUE
                    );
                """)

                # Crear tabla de tipos de caso
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tipos_caso (
                        id_tipo_caso INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_tipo_caso VARCHAR(50) UNIQUE
                    );
                """)

                connection.commit()
                print("Estructura de la base de datos inicializada correctamente.")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
