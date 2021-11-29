from typing import List

from flask_pymongo import PyMongo
from project.database import mongo_client

from ..domain.shipment_event import ShipmentEvent
from ..domain.shipment_event_store import ShipmentEventStore


class ShipmentEventMongoStore(ShipmentEventStore):
    _mongo_client: PyMongo

    def __init__(self):
        self._mongo_client = mongo_client

    def append(self, event: ShipmentEvent) -> None:
        self._mongo_client.db.shipment_events.insert_one(event.to_dict())

    def find_by_shipment_id(self, shipment_id: str) -> List[ShipmentEvent]:
        events = self._mongo_client.db.shipment_events.find(
            {"shipment_id": shipment_id}
        )
        return [ShipmentEvent.from_dict(event) for event in events]
