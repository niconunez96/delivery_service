# Flask application

Prueba de concepto de una aplicacion flask.

## Cómo correr la aplicación
Se puede correr la aplicacion utilizando docker-compose o localmente

**Localmente**

1. Si es la primera vez se debe crear un virtual environment:

    `python3 -m venv env`

2. Activar el entorno virtual

    `source ./env/bin/activate`

3. Instalar las dependencias

    `pip install -r requirements.txt`

4. Para correr la aplicacion localmente se debe crear una base de datos con el nombre que desee y luego se debe editar las variables de entorno en el archivo `.env` (No se deben pushear los cambios de este archivo)

5. Una vez configuradas las variables de entorno se deben correr las migraciones:

    `python ./project/manage.py db upgrade`

6. Correr el servidor con:

    `flask run`

**Via docker-compose**
1. Correr:

    `make runserver`

2. Para attacharse al servidor correr:
    
    `make server-logs`

3. Para finalizar los containers:
    
    `make stopserver`

## Cómo ver los datos de la base de datos de Docker
`make db-client`
