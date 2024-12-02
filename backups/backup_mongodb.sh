#!/bin/bash

# Cargar las variables de entorno desde el archivo .env
export $(grep -v '^#' .env | xargs)

# Variables del script
DATE=$(date +%Y%m%d_%H%M%S)  # Timestamp para el respaldo

# Crear el directorio de respaldo si no existe
mkdir -p "$BACKUP_PATH"

# Realizar el respaldo
mongodump --uri="$MONGO_BACKUP_URI" --out "$BACKUP_PATH/mongo_backup_$DATE"

# Verificar el éxito del respaldo
if [ $? -eq 0 ]; then
    echo "Respaldo de MongoDB completado exitosamente en $BACKUP_PATH/mongo_backup_$DATE"
else
    echo "Error al realizar el respaldo de MongoDB"
    exit 1
fi
