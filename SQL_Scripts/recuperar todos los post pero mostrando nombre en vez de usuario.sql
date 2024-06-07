
SELECT posts.id_post,usuarios.nombre,posts.titulo,posts.texto,posts.fecha
FROM posts INNER JOIN usuarios
ON posts.id_usuario = usuarios.id_usuario