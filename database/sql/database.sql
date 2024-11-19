-- Verificar si la base de datos ya existe y crearla solo si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'customer_care')
BEGIN
    CREATE DATABASE customer_care;
END
GO

-- Cambiar al contexto de la base de datos 'customer_care'
USE customer_care;
GO

-- Crear tabla para canales de contacto
CREATE TABLE canales (
    id_canal INT IDENTITY(1,1) PRIMARY KEY,
    nombre_canal VARCHAR(50) NOT NULL UNIQUE
);

-- Crear tabla para tipos de caso
CREATE TABLE tipos_caso (
    id_tipo_caso INT IDENTITY(1,1) PRIMARY KEY,
    nombre_tipo_caso VARCHAR(50) NOT NULL UNIQUE
);

-- Crear tabla para casos, referenciando id_canal y id_tipo_caso como claves foráneas
CREATE TABLE casos (
    id_caso INT IDENTITY(1,1) PRIMARY KEY,
    fecha_contacto DATETIME NOT NULL,
    id_canal INT NOT NULL,
    PNR VARCHAR(10) NOT NULL,
    id_tipo_caso INT NOT NULL,
    comentarios_agente TEXT,
    FOREIGN KEY (id_canal) REFERENCES canales(id_canal),
    FOREIGN KEY (id_tipo_caso) REFERENCES tipos_caso(id_tipo_caso)
);
