from .shipment import Shipment, ShipmentId


class ShipmentRepo:
    def store(self, shipment: Shipment) -> None:
        raise NotImplementedError

    def update(self, shipment: Shipment) -> None:
        raise NotImplementedError

    def find_by_id(self, id: ShipmentId) -> Shipment:
        """
        :raises: EntityNotFound
        """
        raise NotImplementedError
