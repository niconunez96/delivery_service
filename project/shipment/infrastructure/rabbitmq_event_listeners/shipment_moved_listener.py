import json
from datetime import datetime

from project.shared.infrastructure.event_listener import domain_event_listener

from ...application.shipment_event_creator import ShipmentEventCreator
from ...domain.events.shipment_moved import ShipmentMoved


class ShipmentMovedListener:
    @staticmethod
    @domain_event_listener(event_type=ShipmentMoved.DOMAIN_EVENT)
    def listen(ch, method, properties, body):
        data = json.loads(body)
        try:
            event = ShipmentMoved(
                data["shipment_id"],
                datetime.strptime(data["when"], "%Y-%m-%dT%H:%M:%S.%f"),
                data["country"],
                data["city"],
                data["address"],
            )
            print(f"Event received: {event}")
            event_creator = ShipmentEventCreator()
            event_creator.shipment_moved(event)
        except KeyError:
            print("Invalid event data: {}".format(data))
            return
