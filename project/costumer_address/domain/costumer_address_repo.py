from .costumer_address import CostumerAddress
from .costumer_address_id import CostumerAddressId


class CostumerAddressRepo:
    def store(self, costumer: CostumerAddress) -> None:
        raise NotImplementedError

    def update(self, costumer: CostumerAddress) -> None:
        raise NotImplementedError

    def find_by_id(self, id: CostumerAddressId) -> CostumerAddress:
        """
        raises: EntityNotFound
        """
        raise NotImplementedError

    def find_by_user_id(self, user_id: str) -> CostumerAddress:
        """
        raises: EntityNotFound
        """
        raise NotImplementedError
