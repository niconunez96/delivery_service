from typing import Optional
from ..domain.costumer_address_repo import CostumerAddressRepo
from ..domain.costumer_address_response import CostumerAddressResponse
from ..infrastructure.costumer_address_mongo_repo import CostumerAddressMongoRepo


class CostumerAddressFinder:
    _costumer_address_repo: CostumerAddressRepo

    def __init__(
        self, costumer_address_repo: Optional[CostumerAddressRepo] = None
    ):
        self.costumer_address_repo = costumer_address_repo or CostumerAddressMongoRepo()

    def find_by_user_id(self, user_id: str) -> CostumerAddressResponse:
        costumer_address = self.costumer_address_repo.find_by_user_id(user_id)
        return costumer_address.to_response()
