import json
from datetime import datetime

from project.shared.infrastructure.event_listener import domain_event_listener

from ...application.shipment_event_creator import ShipmentEventCreator
from ...domain.events.shipment_created import ShipmentCreated


class ShipmentCreatedListener:
    @staticmethod
    @domain_event_listener(event_type=ShipmentCreated.DOMAIN_EVENT)
    def listen(ch, method, properties, body):
        data = json.loads(body)
        try:
            event = ShipmentCreated(
                data["shipment_id"],
                datetime.strptime(data["when"], "%Y-%m-%dT%H:%M:%S.%f"),
            )
            print(f"Event received {event}")
            event_creator = ShipmentEventCreator()
            event_creator.shipment_prepared(event)
        except KeyError:
            print("Invalid event data: {}".format(data))
            return
