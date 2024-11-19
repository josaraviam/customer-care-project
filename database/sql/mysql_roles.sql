-- Crear usuario para agentes con permisos de lectura y escritura
CREATE USER 'agent_user'@'%' IDENTIFIED BY 'password123';
GRANT SELECT, INSERT, UPDATE, DELETE ON customer_care.* TO 'agent_user'@'%';

-- Crear usuario para supervisores con permisos de solo lectura
CREATE USER 'supervisor_user'@'%' IDENTIFIED BY 'password123';
GRANT SELECT ON customer_care.* TO 'supervisor_user'@'%';

-- Crear usuario para administradores con todos los permisos
CREATE USER 'admin'@'%' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON customer_care.* TO 'admin'@'%';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;
