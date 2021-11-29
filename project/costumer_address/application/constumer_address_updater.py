from ..domain.costumer_address_id import CostumerAddressId
from ..domain.costumer_address_repo import CostumerAddressRepo
from .dto import CostumerAddressInfo


class CostumerAddressUpdater:
    _costumer_address_repo: CostumerAddressRepo

    def __init__(self, costumer_address_repo: CostumerAddressRepo):
        self._costumer_address_repo = costumer_address_repo

    def update(
        self,
        id: CostumerAddressId,
        info: CostumerAddressInfo,
    ) -> None:
        costumer_address = self._costumer_address_repo.find_by_id(id)
        costumer_address.update(info.to_dict())
        self._costumer_address_repo.update(costumer_address)
