// Conexión a la base de datos MongoDB
use customerCareComments;

// Crear la colección "comentarios" si no existe
db.createCollection("comentarios");

// Crear la colección "usuarios" si no existe
db.createCollection("usuarios");

// Crear la colección "historial_ediciones" si no existe
db.createCollection("historial_ediciones");

// Insertar datos de ejemplo en "comentarios"
db.comentarios.insertOne({
    id_caso: "001",
    texto: "Cliente solicita un reembolso por retraso en vuelo.",
    tags: ["reembolso", "urgente"],
    fecha_creacion: ISODate("2024-12-02T10:00:00Z"),
    usuario: "J0002" // Usamos el id_usuario del agente
});

db.comentarios.insertOne({
    id_caso: "002",
    texto: "Consulta sobre equipaje perdido.",
    tags: ["equipaje", "consulta"],
    fecha_creacion: ISODate("2024-12-02T11:00:00Z"),
    usuario: "J0003" // Usamos el id_usuario del supervisor
});

// Insertar datos de ejemplo en "usuarios"
db.usuarios.insertOne({
    id_usuario: "J0001",
    nombre: "Administrador",
    email: "admin@savimind.ai",
    hashed_password: "$2b$12$L3MQU3R2QX6R9Y1gG5MOtOyq.m58CdW3hAX7.CY8Qe/5RmSC1DS2C", // Hash de "admin123"
    is_admin: true,
    fecha_creacion: ISODate("2024-12-01T08:00:00Z")
});

db.usuarios.insertOne({
    id_usuario: "J0002",
    nombre: "Agente",
    email: "agent@savimind.ai",
    hashed_password: "$2b$12$dWuIUReC5N.MO90LZeqki.tJ.R8nZDjC9MpaSiI2hln.rkFpJxTSG", // Hash de "agent123"
    is_admin: false,
    fecha_creacion: ISODate("2024-12-01T09:00:00Z")
});

db.usuarios.insertOne({
    id_usuario: "J0003",
    nombre: "Supervisor",
    email: "supervisor@savimind.ai",
    hashed_password: "$2b$12$NC/mA3z6B7yBKEhhOLQkSe.Bu09YsPg8VKHkGmPYRzCRY9S.wGjey", // Hash de "supervisor123"
    is_admin: false,
    fecha_creacion: ISODate("2024-12-01T10:00:00Z")
});

// Insertar datos de ejemplo en "historial_ediciones"
db.historial_ediciones.insertOne({
    comentario_id: "001",
    usuario: "J0002", // El agente que editó el comentario
    cambios: {
        texto: "Cliente solicita un reembolso por retraso en vuelo.",
        tags: ["reembolso", "urgente"]
    },
    fecha_edicion: ISODate("2024-12-02T12:00:00Z")
});

db.historial_ediciones.insertOne({
    comentario_id: "002",
    usuario: "J0003", // El supervisor que editó el comentario
    cambios: {
        texto: "Consulta sobre equipaje perdido.",
        tags: ["equipaje", "consulta"]
    },
    fecha_edicion: ISODate("2024-12-02T13:00:00Z")
});
