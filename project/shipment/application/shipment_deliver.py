from project.shared.domain.event_bus import EventBus

from ..domain.shipment import ShipmentId
from ..domain.shipment_repo import ShipmentRepo


class InvalidShipmentStatusToDeliver(Exception):
    pass


class ShipmentDeliver:
    _shipment_repo: ShipmentRepo
    _event_bus: EventBus

    def __init__(self, shipment_repo: ShipmentRepo, event_bus: EventBus):
        self._shipment_repo = shipment_repo
        self._event_bus = event_bus

    def deliver(self, shipment_id: ShipmentId) -> None:
        shipment = self._shipment_repo.find_by_id(shipment_id)
        try:
            shipment.deliver()
        except ValueError:
            raise InvalidShipmentStatusToDeliver
        self._shipment_repo.update(shipment)
        self._event_bus.publish(shipment.delivered_event())
