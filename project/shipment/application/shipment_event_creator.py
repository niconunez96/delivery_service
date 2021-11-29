from typing import Optional

from ..domain.events import ShipmentCreated, ShipmentDelivered, ShipmentMoved
from ..domain.shipment_event import ShipmentEvent
from ..domain.shipment_event_store import ShipmentEventStore
from ..infrastructure.shipment_event_mongo_store import ShipmentEventMongoStore


class ShipmentEventCreator:
    _shipment_event_store: ShipmentEventStore

    def __init__(self, shipment_event_store: Optional[ShipmentEventStore] = None):
        self._shipment_event_store = shipment_event_store or ShipmentEventMongoStore()

    def shipment_prepared(self, event_data: ShipmentCreated):
        shipment_event = ShipmentEvent.create_shipment_preparing(
            event_data.shipment_id, event_data.when
        )
        print(shipment_event)
        self._shipment_event_store.append(shipment_event)

    def shipment_moved(self, event_data: ShipmentMoved):
        shipment_event = ShipmentEvent.create_shipment_on_trip(
            event_data.shipment_id,
            event_data.when,
            event_data.country,
            event_data.city,
            event_data.address,
        )
        self._shipment_event_store.append(shipment_event)

    def shipment_delivered(self, event_data: ShipmentDelivered):
        shipment_event = ShipmentEvent.create_shipment_delivered(
            event_data.shipment_id, event_data.when
        )
        self._shipment_event_store.append(shipment_event)
