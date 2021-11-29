# Flask application 🐍

Prueba de concepto de una aplicacion flask con DDD y event sourcing.

# Documentacion 📜
**Endpoints**
1. POST `/api/costumer_addresses/`
Body
```
{
    "country": "Argentina",
    "city": "Buenos Aires",
    "street": "Calle falsa",
    "house_number": "1698",
    "zip_code": 5501,
    "user_id": "4"
}
```
2. GET `/api/cosumer_addresses/user/:id/`
3. GET `/api/shipments/order/:id/`
4. GET `/api/shipments/:id/trip/`
5. POST `/api/shipments/:id/move/`
Body
```
{
    "country": "Argentina",
    "city": "Mendoza",
    "address": "Pedro molina"
}
```
7. POST `/api/shipments/:id/deliver/`

**Eventos a consumir**
1. Order placed
    * Exchange: `domain_events`
    * Routing key: `order_placed`
    * Body message: {"user_id": str, "order_id": str}

**Eventos despachados**
1. Shipment prepared
    * Exchange: `domain_events`
    * Routing key: `shipment_created`
3. Shipment moved
    * Exchange: `domain_events`
    * Routing key: `shipment_moved`
5. Shipment delivered
    * Exchange: `domain_events`
    * Routing key: `shipment_delivered`

## Cómo correr la aplicación 🏃‍♂️
Se puede correr la aplicacion utilizando docker-compose o de forma local

**Localmente**

1. Si es la primera vez se debe crear un virtual environment:

    `python3 -m venv env`

2. Activar el entorno virtual

    `source ./env/bin/activate`

3. Instalar las dependencias

    `pip install -r requirements.txt`

4. Para correr la aplicacion localmente se debe crear una base de datos mongo con el nombre que desee y luego se debe editar las variables de entorno en el archivo `.env` (No se deben pushear los cambios de este archivo), tambien tiene que estar corriendo rabbitmq 🐰


5. Correr el servidor con:

    `python server.py`

**Via docker-compose** 🐳
1. Correr:

    `make runserver`

2. Para attacharse al servidor correr:
    
    `make server-logs`

3. Para finalizar los containers:
    
    `make stopserver`

4. Para ver los mensajes en rabbitmq se debe ingresar a `localhost:8080` con las credenciales `guest` - `guest`
