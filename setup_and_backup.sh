#!/bin/bash

# Cargar variables desde el archivo .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Archivo .env no encontrado. Asegúrate de que exista en el mismo directorio que este script."
    exit 1
fi

# Función para ejecutar scripts de MySQL
setup_mysql() {
    echo "Configurando la base de datos MySQL..."
    mysql -h "$MYSQL_HOST" -u "$MYSQL_LOCAL_USER" -p"$MYSQL_LOCAL_PASSWORD" < database/sql/database.sql
    mysql -h "$MYSQL_HOST" -u "$MYSQL_LOCAL_USER" -p"$MYSQL_LOCAL_PASSWORD" < database/sql/mysql_roles.sql
    echo "Base de datos MySQL y roles configurados exitosamente."
}

# Función para ejecutar scripts de MongoDB Atlas
setup_mongodb() {
    echo "Configurando la base de datos MongoDB Atlas..."
    mongo "${MONGO_URI}" < database/mongodb/mongodb_setup.js
    mongo "${MONGO_URI}" < database/mongodb/mongodb_roles.js
    echo "Base de datos MongoDB Atlas y roles configurados exitosamente."
}

# Función para realizar respaldo de MySQL
backup_mysql() {
    echo "Realizando respaldo de MySQL..."
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_file="backups/mysql_backup_${timestamp}.sql"
    mysqldump -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DB" > "$backup_file"
    if [ $? -eq 0 ]; then
        echo "Respaldo de MySQL completado: $backup_file"
    else
        echo "Error al realizar el respaldo de MySQL."
    fi
}

# Función para realizar respaldo de MongoDB Atlas
backup_mongodb() {
    echo "Realizando respaldo de MongoDB Atlas..."
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_folder="backups/mongodb_backup_${timestamp}"
    mongodump --uri="${MONGO_BACKUP_URI}" --out "$backup_folder"
    if [ $? -eq 0 ]; then
        echo "Respaldo de MongoDB Atlas completado: $backup_folder"
    else
        echo "Error al realizar el respaldo de MongoDB Atlas."
    fi
}

# Ejecución de funciones
echo "Iniciando configuración y respaldos..."
setup_mysql
setup_mongodb
backup_mysql
backup_mongodb
echo "Configuración y respaldos completados."
