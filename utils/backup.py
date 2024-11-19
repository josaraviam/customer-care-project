import os
from datetime import datetime
import subprocess


# Función para respaldar la base de datos MySQL
def backup_mysql():
    try:
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)

        # Archivo de respaldo con marca de tiempo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"mysql_backup_{timestamp}.sql")

        # Comando mysqldump
        command = f"mysqldump -h {os.getenv('MYSQL_HOST')} -u {os.getenv('MYSQL_USER')} -p{os.getenv('MYSQL_PASSWORD')} {os.getenv('MYSQL_DB')} > {backup_file}"
        subprocess.run(command, shell=True, check=True)

        print(f"Respaldo de MySQL completado: {backup_file}")
    except Exception as e:
        print(f"Error durante el respaldo de MySQL: {e}")


# Función para respaldar la base de datos MongoDB
def backup_mongodb():
    try:
        backup_dir = "backups/mongodb"
        os.makedirs(backup_dir, exist_ok=True)

        # Directorio de respaldo con marca de tiempo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"mongodb_backup_{timestamp}")

        # Comando mongodump
        command = f"mongodump --uri=\"{os.getenv('MONGO_URI')}\" --out {backup_path}"
        subprocess.run(command, shell=True, check=True)

        print(f"Respaldo de MongoDB completado: {backup_path}")
    except Exception as e:
        print(f"Error durante el respaldo de MongoDB: {e}")


if __name__ == "__main__":
    print("Iniciando respaldo...")
    backup_mysql()
    backup_mongodb()
    print("Respaldo completado.")
