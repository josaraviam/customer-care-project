import pymysql
from contextlib import contextmanager
from app.config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB


def get_mysql_connection():
    """
    Conecta a la base de datos MySQL en Amazon RDS.
    """
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=int(MYSQL_PORT),
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar a MySQL: {e}")
        raise


@contextmanager
def mysql_connection():
    """
    Context manager para manejar conexiones automáticamente.
    """
    connection = get_mysql_connection()
    try:
        yield connection
    finally:
        connection.close()


def initialize_database():
    """
    Inicializa las tablas de la base de datos si no existen.
    """
    try:
        with mysql_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS casos (
                        id_caso INT AUTO_INCREMENT PRIMARY KEY,
                        fecha_contacto DATE,
                        canal_contacto VARCHAR(255),
                        pnr VARCHAR(255),
                        tipo_caso VARCHAR(255),
                        comentarios TEXT
                    )
                """)
                connection.commit()
        print("Tablas inicializadas correctamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
