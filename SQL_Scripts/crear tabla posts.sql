CREATE TABLE posts (
id_post INT NOT NULL AUTO_INCREMENT,
id_usuario INT NOT NULL, 
titulo VARCHAR(60) NOT NULL,
texto TEXT NOT NULL,
fecha DATETIME DEFAULT NOW(), 
PRIMARY KEY (id_post),
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
)