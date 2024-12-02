-- Crear usuario para agentes
CREATE USER 'agent_user'@'%' IDENTIFIED BY 'password123';
GRANT SELECT, INSERT, UPDATE, DELETE ON customer_care.* TO 'agent_user'@'%';

-- Crear usuario para supervisores
CREATE USER 'supervisor_user'@'%' IDENTIFIED BY 'password123';
GRANT SELECT ON customer_care.* TO 'supervisor_user'@'%';

-- Crear usuario para administradores
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON customer_care.* TO 'admin'@'%';

-- Aplicar cambios de privilegios
FLUSH PRIVILEGES;
