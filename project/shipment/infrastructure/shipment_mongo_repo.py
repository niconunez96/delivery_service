from flask_pymongo import PyMongo
from project.database import mongo_client
from project.shared.errors import EntityNotFound

from ..domain.shipment import Shipment, ShipmentId
from ..domain.shipment_repo import ShipmentRepo


class ShipmentMongoRepo(ShipmentRepo):
    _mongo_client: PyMongo

    def __init__(self):
        self._mongo_client = mongo_client

    def store(self, shipment: Shipment) -> None:
        self._mongo_client.db.shipments.insert_one(shipment.to_dict())

    def update(self, shipment: Shipment) -> None:
        self._mongo_client.db.shipments.find_one_and_replace(
            {'id': str(shipment.id)},
            shipment.to_dict()
        )

    def find_by_id(self, id: ShipmentId) -> Shipment:
        """
        :raises: EntityNotFound
        """
        result = self._mongo_client.db.shipments.find_one({"id": str(id)})
        if not result:
            raise EntityNotFound
        return Shipment.from_dict(result)
