from dataclasses import dataclass

from .costumer_address_id import CostumerAddressId


@dataclass(frozen=True)
class CostumerAddressResponse:
    id: CostumerAddressId
    user_id: str
    country: str
    city: str
    street: str
    house_number: str
    zip_code: int
