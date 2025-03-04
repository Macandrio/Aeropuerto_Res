Pasos a seguir al descargar el proyecto desde git

1. Nos situaremos en la crpeta Aeropuerto_Cliente
2. Crearemos la carpeta myven con:
    * python3 -m venv myvenv
3. Activaremos el entrono con:
    * source myvenv/bin/activate
4. Instalaremos los requirement y actualizaremos con:
    * python -m pip install --upgrade pip
    * pip install -r requirements.txt
5. Crearemos la base de datos con:
    * python manage.py makemigrations
    * python manage.py migrate
6. Debemos usar los datos ya guardados para los grupos y los permisos con:
    * python manage.py loaddata apaeropuerto/fixtures/grupos_permisos_usuarios.json

Apartir de aqui ya puedes usar la aplicacion
 
puedes usar los datos ya guardados con:
    * python manage.py loaddata apaeropuerto/fixtures/grupos_permisos_usuarios.json