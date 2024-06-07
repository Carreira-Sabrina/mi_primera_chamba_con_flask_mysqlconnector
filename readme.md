# COMO CLONAR ESTE REPOSITORIO !

- clonar el repositorio de la forma preferida
- Abrir una consola tipo cmd (no powershell por favor ! )
- Crear un entorno virtual:
        - python -m venv nombreentorno virtual
- Entrar en el entorno virtual: 
        - .\nombreentornovirtual\Scripts\activate
- Instalar las dependencias:
        - pip install -r requirements.txt

- También vas a necesitar una base de datos, está incluida en la carpeta dump_BD, se puede importar desde MySQL Workbench
desde Administration/MANAGEMENT/Data Import/Restore

-Los parámetros de mi conexion están en el archivo config_base_datos, tus parámetros de conexión (especialmente el password)
podrían cambiar