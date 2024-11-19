// Conexión a la base de datos
use customerCareComments;

// Crear colección de comentarios
db.createCollection("comentarios");

// Ejemplo de documento en la colección de comentarios
db.comentarios.insertOne({
    id_caso: "ID del caso correspondiente",
    comentarios: "Texto de los comentarios adicionales",
    tags: ["Etiqueta1", "Etiqueta2"]
});
