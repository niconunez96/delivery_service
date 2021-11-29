import os
import threading
import pika


def domain_event_listener(event_type: str):
    def decorator(consumer):
        def wrapper(*args, **kwargs):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST", "localhost"))
                )
                channel = connection.channel()

                channel.exchange_declare(
                    exchange="domain_events",
                    exchange_type="direct",
                )

                result = channel.queue_declare(event_type)
                queue_name = result.method.queue
                channel.queue_bind(
                    exchange="domain_events",
                    queue=queue_name,
                    routing_key=event_type,
                )
                print(f"RabbitMQ connected to domain events exchange for queue {event_type}")
                channel.basic_consume(queue_name, consumer, auto_ack=True)
                channel.start_consuming()
            except Exception as e:
                from project.rabbitmq import initDomainListeners

                print(e)
                print("Something went wrong with the connection, retrying in 5 secs")
                threading.Timer(5.0, initDomainListeners).start()

        return wrapper

    return decorator
