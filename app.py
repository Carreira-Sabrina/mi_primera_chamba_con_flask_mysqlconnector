from flask import Flask,render_template
import mysql.connector
from config_base_datos import cursor_base_de_datos

#Se crea la aplicacion
aplicacion = Flask (__name__)


#Rutas

#index.html
@aplicacion.route("/")
def index():
    #RECUPERO LOS POSTS DE LA BASE DE DATOS
    posts_en_bd = get_posts()
    #EL SEGUNDO PARAMETRO SON LOS DATOS DE LA BD QUE PASO PARA CARGAR DINAMICAMENTE CON JINJA EN EL HTML
    return render_template("index.html",posts = posts_en_bd)


#ESTA FUNCION PERMITE RECUPERAR LOS POSTS DE LA BASE DE DATOS
def get_posts():
    #consulta = ("SELECT * FROM posts")
    consulta = ("SELECT posts.id_post,usuarios.nombre,posts.titulo,posts.texto,posts.fecha FROM posts INNER JOIN usuarios ON posts.id_usuario = usuarios.id_usuario")
    cursor_base_de_datos.execute(consulta)
    resultado_consulta = cursor_base_de_datos.fetchall()
    
    for fila in resultado_consulta:
        print(fila)
    #ME CONVENDRIA DEVOLVER EL RESULTADO DE LA CONSULTA???
    return resultado_consulta



if __name__ in "__main__":
    aplicacion.run(debug=True)