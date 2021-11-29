from ..domain.shipment_repo import ShipmentRepo
from ..domain.shipment import ShipmentId
from ..domain.shipment_response import ShipmentResponse


class ShipmentFinder:
    _shipment_repo: ShipmentRepo

    def __init__(self, shipment_repo: ShipmentRepo):
        self._shipment_repo = shipment_repo

    def find(self, shipment_id: ShipmentId) -> ShipmentResponse:
        shipment = self._shipment_repo.find_by_id(shipment_id)
        return shipment.to_response()

    def find_by_order(self, order_id: str) -> ShipmentResponse:
        shipment = self._shipment_repo.find_by_order_id(order_id)
        return shipment.to_response()
