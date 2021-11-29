from dataclasses import dataclass

from project.shared.domain.event_bus import EventBus

from ..domain.shipment import ShipmentId
from ..domain.shipment_repo import ShipmentRepo


class InvalidShipmentStatus(Exception):
    pass


@dataclass(frozen=True)
class ShipmentLocationInfo:
    country: str
    city: str
    address: str

    @staticmethod
    def from_dict(body: dict) -> 'ShipmentLocationInfo':
        return ShipmentLocationInfo(
            country=body['country'],
            city=body['city'],
            address=body['address'],
        )


class ShipmentLocationUpdater:
    _shipment_repo: ShipmentRepo
    _event_bus: EventBus

    def __init__(self, shipment_repo: ShipmentRepo, event_bus: EventBus):
        self._shipment_repo = shipment_repo
        self._event_bus = event_bus

    def move_shipment(
        self, shipment_id: ShipmentId, new_location: ShipmentLocationInfo
    ) -> None:
        shipment = self._shipment_repo.find_by_id(shipment_id)
        try:
            shipment.on_trip()
        except ValueError:
            raise InvalidShipmentStatus()
        self._shipment_repo.update(shipment)
        self._event_bus.publish(shipment.moved_event(
            new_location.country,
            new_location.city,
            new_location.address,
        ))
