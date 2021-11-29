import json
import threading

import pika

from project.shipment.infrastructure.rabbitmq_event_listeners import (  # noqa
    ShipmentCreatedListener,
    ShipmentDeliveredListener,
    ShipmentMovedListener,
)


def initAuth():
    """
    Inicializa RabbitMQ para escuchar eventos logout.
    """
    authConsumer = threading.Thread(target=listenAuth)
    authConsumer.start()


def initDomainListeners():
    """
    Inicializa RabbitMQ para escuchar eventos de dominio.
    """
    shipment_created_listener = ShipmentCreatedListener()
    shipment_created = threading.Thread(target=shipment_created_listener.listen)
    shipment_moved_listener = ShipmentMovedListener()
    shipment_moved = threading.Thread(target=shipment_moved_listener.listen)
    shipment_delivered_listener = ShipmentDeliveredListener()
    shipment_delivered = threading.Thread(target=shipment_delivered_listener.listen)

    shipment_created.start()
    shipment_moved.start()
    shipment_delivered.start()


def listenAuth():
    """
    Básicamente eventos de logout enviados por auth.
    @api {fanout} auth/logout Logout
    @apiGroup RabbitMQ GET
    @apiDescription Escucha de mensajes logout desde auth.Invalida sesiones en cache.  # noqa
    @apiExample {json} Mensaje
      {
        "type": "article-exist",
        "message" : "tokenId"
      }
    """
    AUTH_EXCHANGE = "auth"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )
        channel = connection.channel()

        channel.exchange_declare(
            exchange=AUTH_EXCHANGE,
            exchange_type="fanout",
        )

        result = channel.queue_declare("", exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=AUTH_EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.loads(body.decode("utf-8"))
            print(event)

        print("RabbitMQ Auth conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()
    except Exception as e:
        print("RabbitMQ Auth desconectado,intentando reconectar en 10'")
        print(e)
        threading.Timer(10.0, initAuth).start()
