import json
from project.shared.event_listener import domain_event_listener
from project.shared.events.order_placed import OrderPlaced
from project.shipment.application.shipment_starter import ShipmentStarter
from project.shipment.application.shipment_starter import ShipmentInfo
from project.shipment.domain.shipment import ShipmentId


class OrderPlacedListener:
    @staticmethod
    @domain_event_listener(event_type=OrderPlaced.DOMAIN_EVENT)
    def listen(ch, method, properties, body):
        data = json.loads(body)
        try:
            event = OrderPlaced(
                data["order_id"],
                data["user_id"],
            )
            print(f"Event received {event}")
            shipment_starter = ShipmentStarter()
            shipment_id = ShipmentId()
            shipment_starter.start_shipment(
                shipment_id, ShipmentInfo(event.order_id, event.user_id)
            )
        except KeyError:
            print("Invalid event data: {}".format(data))
            return
