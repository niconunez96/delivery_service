from ..domain.costumer_address_id import CostumerAddressId
from ..domain.costumer_address import CostumerAddress
from ..domain.costumer_address_repo import CostumerAddressRepo
from .dto import CostumerAddressInfo
from project.shared.errors import EntityNotFound


class CostumerAddressAlreadyExists(Exception):
    pass


class CostumerAddressCreator:
    _costumer_address_repo: CostumerAddressRepo

    def __init__(self, costumer_address_repo: CostumerAddressRepo):
        self._costumer_address_repo = costumer_address_repo

    def create(
        self,
        id: CostumerAddressId,
        info: CostumerAddressInfo,
    ) -> None:
        try:
            costumer_address = self._costumer_address_repo.find_by_user_id(
                info.user_id,
            )
        except EntityNotFound:
            costumer_address = None

        if costumer_address:
            raise CostumerAddressAlreadyExists
        costumer_address = CostumerAddress(
            id,
            info.user_id,
            info.country,
            info.city,
            info.street,
            info.house_number,
            info.zip_code,
        )
        self._costumer_address_repo.store(costumer_address)
