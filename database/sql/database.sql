-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS customer_care;

-- Usar la base de datos
USE customer_care;

-- Tabla de canales de contacto
CREATE TABLE IF NOT EXISTS canales (
    id_canal INT AUTO_INCREMENT PRIMARY KEY,
    nombre_canal VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de tipos de caso
CREATE TABLE IF NOT EXISTS tipos_caso (
    id_tipo_caso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo_caso VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de casos
CREATE TABLE IF NOT EXISTS casos (
    id_caso INT AUTO_INCREMENT PRIMARY KEY,
    fecha_contacto DATETIME NOT NULL,
    id_canal INT NOT NULL,
    PNR VARCHAR(10) NOT NULL,
    id_tipo_caso INT NOT NULL,
    comentarios_agente TEXT,
    FOREIGN KEY (id_canal) REFERENCES canales(id_canal),
    FOREIGN KEY (id_tipo_caso) REFERENCES tipos_caso(id_tipo_caso)
);

-- Insertar datos de ejemplo
INSERT INTO canales (nombre_canal) VALUES ('Facebook'), ('Twitter'), ('WhatsApp');
INSERT INTO tipos_caso (nombre_tipo_caso) VALUES ('Consulta'), ('Reclamo');
INSERT INTO casos (fecha_contacto, id_canal, PNR, id_tipo_caso, comentarios_agente)
VALUES ('2024-12-02 12:00:00', 1, 'ABC123', 2, 'Cliente solicita reembolso.');
