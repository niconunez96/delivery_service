from typing import List
from .shipment_event import ShipmentEvent


class ShipmentEventStore:

    def append(self, event: ShipmentEvent) -> None:
        raise NotImplementedError

    def find_by_shipment_id(self, shipment_id: str) -> List[ShipmentEvent]:
        raise NotImplementedError
