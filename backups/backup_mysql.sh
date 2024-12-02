#!/bin/bash

# Cargar las variables de entorno desde el archivo .env
export $(grep -v '^#' .env | xargs)

# Variables del script
DATE=$(date +%Y%m%d_%H%M%S)  # Timestamp para el respaldo
BACKUP_FILE="mysql_backup_$DATE.sql"

# Crear el respaldo de MySQL
mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DB" > "$BACKUP_PATH/$BACKUP_FILE"

# Verificar el éxito del respaldo
if [ $? -eq 0 ]; then
    echo "Respaldo de MySQL completado exitosamente en $BACKUP_PATH/$BACKUP_FILE"
else
    echo "Error al realizar el respaldo de MySQL"
    exit 1
fi
