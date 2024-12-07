-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS customer_care;

-- Usar la base de datos
USE customer_care;

-- Tabla de canales de contacto
CREATE TABLE IF NOT EXISTS canales (
    id_canal INT AUTO_INCREMENT PRIMARY KEY, -- ID único del canal de contacto
    nombre_canal VARCHAR(50) NOT NULL UNIQUE -- Nombre del canal (ej. Facebook, WhatsApp)
);

-- Tabla de tipos de caso
CREATE TABLE IF NOT EXISTS tipos_caso (
    id_tipo_caso INT AUTO_INCREMENT PRIMARY KEY, -- ID único del tipo de caso
    nombre_tipo_caso VARCHAR(50) NOT NULL UNIQUE -- Nombre del tipo de caso (ej. Consulta, Reclamo)
);

-- Tabla de casos
CREATE TABLE IF NOT EXISTS casos (
    id_caso INT AUTO_INCREMENT PRIMARY KEY, -- ID único del caso
    fecha_contacto DATETIME NOT NULL, -- Fecha y hora del contacto con el cliente
    id_canal INT NOT NULL, -- ID del canal de contacto (FK de la tabla canales)
    PNR VARCHAR(10) NOT NULL, -- PNR único del cliente
    id_tipo_caso INT NOT NULL, -- ID del tipo de caso (FK de la tabla tipos_caso)
    comentarios_agente TEXT, -- Comentarios del agente sobre el caso
    FOREIGN KEY (id_canal) REFERENCES canales(id_canal), -- Relación con la tabla canales
    FOREIGN KEY (id_tipo_caso) REFERENCES tipos_caso(id_tipo_caso) -- Relación con la tabla tipos_caso
);

-- Crear una vista para consultar casos con detalles completos
CREATE OR REPLACE VIEW vista_casos_completa AS
SELECT
    c.id_caso,
    c.fecha_contacto,
    canales.nombre_canal,
    c.PNR,
    tipos_caso.nombre_tipo_caso,
    c.comentarios_agente
FROM
    casos c
INNER JOIN canales ON c.id_canal = canales.id_canal
INNER JOIN tipos_caso ON c.id_tipo_caso = tipos_caso.id_tipo_caso;

-- Crear una secuencia para futuros casos (si no deseas usar AUTO_INCREMENT)
CREATE SEQUENCE IF NOT EXISTS secuencia_casos
START WITH 1000
INCREMENT BY 1;

-- Crear un trigger para registrar la fecha de modificación en la tabla casos
DELIMITER //
CREATE TRIGGER antes_de_actualizar_caso
BEFORE UPDATE ON casos
FOR EACH ROW
BEGIN
    SET NEW.fecha_contacto = CURRENT_TIMESTAMP;
END;
//
DELIMITER ;

-- Crear un procedimiento para agregar un nuevo caso
DELIMITER //
CREATE PROCEDURE insertar_caso(
    IN p_fecha_contacto DATETIME,
    IN p_id_canal INT,
    IN p_PNR VARCHAR(10),
    IN p_id_tipo_caso INT,
    IN p_comentarios_agente TEXT
)
BEGIN
    INSERT INTO casos (fecha_contacto, id_canal, PNR, id_tipo_caso, comentarios_agente)
    VALUES (p_fecha_contacto, p_id_canal, p_PNR, p_id_tipo_caso, p_comentarios_agente);
END;
//
DELIMITER ;

-- Crear una función para contar el número de casos por tipo de caso
DELIMITER //
CREATE FUNCTION contar_casos_por_tipo(tipo_caso_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_casos INT;
    SELECT COUNT(*) INTO total_casos
    FROM casos
    WHERE id_tipo_caso = tipo_caso_id;
    RETURN total_casos;
END;
//
DELIMITER ;

-- Crear un índice en el campo PNR para búsquedas rápidas
CREATE INDEX idx_pnr ON casos (PNR);
