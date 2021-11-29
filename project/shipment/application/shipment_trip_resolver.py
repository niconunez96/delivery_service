from typing import List

from ..domain.shipment_event import ShipmentEvent
from ..domain.shipment_event_store import ShipmentEventStore


class ShipmentTripResolver:
    _shipment_event_store: ShipmentEventStore

    def __init__(self, shipment_event_store: ShipmentEventStore):
        self._shipment_event_store = shipment_event_store

    def execute(self, shipment_id: str) -> List[ShipmentEvent]:
        trip = [shipment_event.to_response() for shipment_event in self._shipment_event_store.find_by_shipment_id(shipment_id)]
        return sorted(trip, key=lambda shipment_event: shipment_event.when)
