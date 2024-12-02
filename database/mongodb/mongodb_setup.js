// Conexión a la base de datos MongoDB
use customerCareComments;

// Crear la colección "comentarios" si no existe
db.createCollection("comentarios");
db.createCollection("usuarios");
db.createCollection("historial_ediciones");


// Insertar datos de ejemplo en la colección de comentarios
db.comentarios.insertOne({
    id_caso: "001",
    texto: "Cliente solicita un reembolso por retraso en vuelo.",
    tags: ["reembolso", "urgente"],
    fecha_creacion: ISODate("2024-12-02T10:00:00Z"),
    usuario: "agent_user"
});

db.comentarios.insertOne({
    id_caso: "002",
    texto: "Consulta sobre equipaje perdido.",
    tags: ["equipaje", "consulta"],
    fecha_creacion: ISODate("2024-12-02T11:00:00Z"),
    usuario: "supervisor_user"
});
