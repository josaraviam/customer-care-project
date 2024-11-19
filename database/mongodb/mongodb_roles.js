// Crear usuario con permisos de lectura y escritura
db.createUser({
    user: "agent_user",
    pwd: "password123",
    roles: [
        { role: "readWrite", db: "customerCareComments" }
    ]
});

// Crear usuario con permisos de lectura y escritura
db.createUser({
    user: "admin",
    pwd: "admin123",
    roles: [
        { role: "readWrite", db: "customerCareComments" }
    ]
});

// Crear usuario con permisos de solo lectura
db.createUser({
    user: "supervisor_user",
    pwd: "password123",
    roles: [
        { role: "read", db: "customerCareComments" }
    ]
});
