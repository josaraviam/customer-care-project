#!/bin/bash

# Función para ejecutar scripts de MySQL
setup_mysql() {
    echo "Configurando la base de datos MySQL..."
    mysql -u root -p < database/sql/database.sql
    mysql -u root -p < database/sql/mysql_roles.sql
    echo "Base de datos MySQL y roles configurados exitosamente."
}

# Función para ejecutar scripts de MongoDB Atlas
setup_mongodb() {
    echo "Configurando la base de datos MongoDB Atlas..."
    mongo "mongodb+srv://agent_user:password123@cluster0.mongodb.net/customerCareComments" < database/mongodb/mongodb_setup.js
    mongo "mongodb+srv://agent_user:password123@cluster0.mongodb.net/customerCareComments" < database/mongodb/mongodb_roles.js
    echo "Base de datos MongoDB Atlas y roles configurados exitosamente."
}

# Función para realizar respaldo de MySQL
backup_mysql() {
    echo "Realizando respaldo de MySQL..."
    mysqldump -u agent_user -p'password123' customer_care > backups/customer_care_backup.sql
    echo "Respaldo de MySQL completado."
}

# Función para realizar respaldo de MongoDB Atlas
backup_mongodb() {
    echo "Realizando respaldo de MongoDB Atlas..."
    mongodump --uri="mongodb+srv://agent_user:password123@cluster0.mongodb.net/customerCareComments" --out backups/mongodb_backup
    echo "Respaldo de MongoDB Atlas completado."
}

# Ejecución de funciones
echo "Iniciando configuración y respaldos..."
setup_mysql
setup_mongodb
backup_mysql
backup_mongodb
echo "Configuración y respaldos completados."
