import mysql.connector

#Parámetros de la conexión con la base de datos (cuidado, su password puede ser distinto !!!!)

parametros_bd = {
    "user": "root",
    "password": "0pt1mu5Pr1m3",
    "host": "localhost",
    "database":"crudpython"
}

#Conectar con la BD 
#base_de_datos =mysql.connector.connect(host="localhost",user="root",password = "0pt1mu5Pr1m3",database="crudpython")
#se ponen ** antes del diccionario pasado como parámetro para que lo tome como **kwargs
base_de_datos =mysql.connector.connect(**parametros_bd)

#Crear un "cursor" para "moverse" por la base de datos
cursor_base_de_datos = base_de_datos.cursor()
