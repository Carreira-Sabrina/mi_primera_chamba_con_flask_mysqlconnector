from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
from config_base_datos import cursor_base_de_datos,base_de_datos

#Se crea la aplicacion
aplicacion = Flask (__name__)

# __________________ TO DO LIST O EN CRIOLLO, ESTE CÓDIGO PARECE UN PLATO DE SPAGETTI _____________
#QUE HAY QUE ARREGLAR ACÁ URGENTE !!! => EN ALGÚN MOMENTO HAY QUE CERRAR LA CONEXIÓN A LA BASE DE DATOS !! 
#OTRA COSA: ESTE ARCHIVO ES UN MASACOTE, PODRIA PONER LAS FUNCIONES CRUD EN OTRO ARCHIVO E IMPORTARLAS?
#ALGO MAS: DEBERÍA INVESTIGAR MÁS SOBRE BLUEPRINTS PARA TENER LAS VISTAS EN OTRO ARCHIVO
#===========================================================================================================

# __________________ FUNCIONES CRUD _____________________________ 

#ESTA FUNCION PERMITE RECUPERAR LOS POSTS DE LA BASE DE DATOS (READ)
def get_posts():
    consulta = ("SELECT posts.id_post,usuarios.nombre,posts.titulo,posts.texto,posts.fecha FROM posts INNER JOIN usuarios ON posts.id_usuario = usuarios.id_usuario")
    cursor_base_de_datos.execute(consulta)
    resultado_consulta = cursor_base_de_datos.fetchall()
    return resultado_consulta


#ESTA FUNCION PERMITE RECUPERAR LOS USUARIOS DE LA BASE DE DATOS
def get_users_id_and_name():
    #POR AHORA ME SIRVE SOLO RECUPERAR ID Y NOMBRE
    consulta_usuarios= ("SELECT id_usuario,nombre FROM usuarios ORDER BY id_usuario")
    cursor_base_de_datos.execute(consulta_usuarios)
    resultado_consulta_usuarios = cursor_base_de_datos.fetchall()
    return resultado_consulta_usuarios

#ESTA FUNCION RECUPERA UN SOLO POST (SE USA POR EJEMPLO PARA EL EDIT)
def get_one_post(id):
    #Obtiene el titulo y el texto de un post a partir de un id para enviar a ser editado
    consulta_titulo_texto_post = ("SELECT titulo,texto FROM posts WHERE id_post = %s")
    #Los datos de las consultas parametrizadas tienen que ir en tuplas
    #SI, ASI DE FEO, SI NO PONGO LA COMA AL FINAL NO LO TOMA COMO TUPLA !!!
    parametros_consulta = (id,)
    cursor_base_de_datos.execute(consulta_titulo_texto_post,parametros_consulta)
    resultado_consulta_post = cursor_base_de_datos.fetchone()
    print("**** Recuperando datos del post")
    print(resultado_consulta_post)
    return resultado_consulta_post

# ________________ Rutas ___________________

#index.html
@aplicacion.route("/")
def index():
    #RECUPERO LOS POSTS DE LA BASE DE DATOS
    posts_en_bd = get_posts()
    #EL SEGUNDO PARAMETRO SON LOS DATOS DE LA BD QUE PASO PARA CARGAR DINAMICAMENTE CON JINJA EN EL HTML
    return render_template("index.html",posts = posts_en_bd)

#crear_post.html
@aplicacion.route("/crear_post")
def crear_post():
    #Antes que nada tengo que recuperar los usuarios de la base de datos para poblar el select
    id_y_nombre_usuarios = get_users_id_and_name()
    #EL SEGUNDO PARAMETRO SON LOS DATOS DE LA BD QUE PASO PARA RELLENAR EL SELECT DINAMICAMENTE CON JINJA EN EL HTML
    return render_template("crear_post.html",datosUsuarios = id_y_nombre_usuarios)

#volcado de nuevo post en BD, maneja la inserción en la base de datos, no es una pagina "que se vea"
@aplicacion.route("/post_creado",methods=["POST"])
def guardar_post_en_BD():
    #POR EL AMOR DE DIOS BENDITO, ESTO FUNCIONA !!!
    autor_post = request.form["seleccion-usuario-post"]
    titulo_post = request.form["titulo-post"]
    texto_post = request.form["texto-post"]
    
    if autor_post and titulo_post and texto_post:
        sql_insertar_post = ("INSERT INTO posts (id_usuario,titulo,texto) VALUES (%s, %s, %s)")
        datos_a_insertar = (autor_post,titulo_post,texto_post)
        cursor_base_de_datos.execute(sql_insertar_post,datos_a_insertar)
        base_de_datos.commit()
    else:
        #NO ME QUEMÉS QUE ESTO ES SÓLO PARA DEBUG
        print("Faltan datos para crear un post guardar")

    #DESPUES DE CREAR UN POST SE REDIRECCIONA AL INDEX, SI YA SE, FALTA ALGO DE FEEDBACK AL USUARIO
    #CUIDADO, INDEX ESTÁ ESPERANDO DATOS !!!!!
    #ACA HAY UN TEMITA, INDEX ESTA ESPERANDO DATOS ! 
    posts_en_bd = get_posts()
    return redirect(url_for("index",posts = posts_en_bd))



@aplicacion.route("/editar_post/<int:id>",methods=["GET","POST"])
def editar_post(id):
    #Se obtienen los datos a editar (titulo y texto del post)
    
    if request.method == "POST":
        nuevo_titulo_post = request.form["titulo_post"]    
        nuevo_texto_post = request.form["texto_post"]    
        #Al pulsar el boton enviar... si hay datos...hago el update
        if nuevo_titulo_post and nuevo_texto_post:
            sql_actualizar_post = ("UPDATE posts SET titulo=%s,texto=%s WHERE id_post=%s")
            parametros_consulta = (nuevo_titulo_post,nuevo_texto_post,id)
            cursor_base_de_datos.execute(sql_actualizar_post,parametros_consulta)
            base_de_datos.commit()
            #ACA HAY UN TEMITA, INDEX ESTA ESPERANDO DATOS ! 
            posts_en_bd = get_posts()
                    
            return redirect (url_for("index",posts = posts_en_bd))
        else:
            print("FALTAN DATOS PARA ACTUALIZAR EL POST")
    else:
        contenido_a_editar = get_one_post(id)
        print("==============CONTENIDO A EDITAR en index 0 =========")
        print(contenido_a_editar[0])
        print("==============CONTENIDO A EDITAR en index 1 =========")
        print(contenido_a_editar[1])
        return render_template("update_post.html", contenido_a_editar=contenido_a_editar)


if __name__ in "__main__":
    aplicacion.run(debug=True)