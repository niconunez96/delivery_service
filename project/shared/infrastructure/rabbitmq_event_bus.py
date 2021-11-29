import os

import pika

from ..domain.event_bus import DomainEvent, EventBus


class RabbitMQEventBus(EventBus):
    DOMAIN_EVENT_EXCHANGE = "domain_events"

    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST", "localhost"))
        )
        self.channel = connection.channel()

        self.channel.exchange_declare(
            exchange=self.DOMAIN_EVENT_EXCHANGE,
            exchange_type="direct",
        )

    def publish(self, event: DomainEvent):
        print(f"Publishing event {event.to_json()}")
        print(
            f"EXHANGE {self.DOMAIN_EVENT_EXCHANGE} --- ROUTING KEY {event.DOMAIN_EVENT}"
        )
        self.channel.basic_publish(
            exchange=self.DOMAIN_EVENT_EXCHANGE,
            routing_key=event.DOMAIN_EVENT,
            body=event.to_json(),
        )
