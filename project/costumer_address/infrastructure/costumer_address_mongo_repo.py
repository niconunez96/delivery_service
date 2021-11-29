from flask_pymongo import PyMongo
from project.database import mongo_client
from project.shared.errors import EntityNotFound

from ..domain.costumer_address import CostumerAddress
from ..domain.costumer_address_id import CostumerAddressId
from ..domain.costumer_address_repo import CostumerAddressRepo


class CostumerAddressMongoRepo(CostumerAddressRepo):
    _mongo_client: PyMongo

    def __init__(self):
        self._mongo_client = mongo_client

    def store(self, costumer: CostumerAddress) -> None:
        self._mongo_client.db.costumer_addresses.insert_one(costumer.to_dict())

    def update(self, costumer_address: CostumerAddress) -> None:
        self._mongo_client.db.costumer_addresses.find_one_and_replace(
            {"id": str(costumer_address.id)}, costumer_address.to_dict()
        )

    def find_by_user_id(self, user_id: str) -> CostumerAddress:
        """
        raises: EntityNotFound
        """
        result = self._mongo_client.db.costumer_addresses.find_one({"user_id": user_id})
        if not result:
            raise EntityNotFound
        return CostumerAddress.from_dict(result)

    def find_by_id(self, id: CostumerAddressId) -> CostumerAddress:
        """
        raises: EntityNotFound
        """
        result = self._mongo_client.db.costumer_addresses.find_one({"id": str(id)})
        if not result:
            raise EntityNotFound
        return CostumerAddress.from_dict(result)
