from .costumer_address_id import CostumerAddressId
from .costumer_address_response import CostumerAddressResponse


class CostumerAddress:
    id: CostumerAddressId
    _user_id: str
    _country: str
    _city: str
    _street: str
    _house_number: str
    _zip_code: int

    def __init__(
        self,
        id: CostumerAddressId,
        user_id: str,
        country: str,
        city: str,
        street: str,
        house_number: str,
        zip_code: str,
    ):
        self.id = id
        self._user_id = user_id
        self._country = country
        self._city = city
        self._street = street
        self._house_number = house_number
        self._zip_code = zip_code

    def update(self, data: dict):
        self._country = data.get("country", self._country)
        self._city = data.get("city", self._city)
        self._street = data.get("street", self._street)
        self._house_number = data.get("house_number", self._house_number)
        self._zip_code = data.get("zip_code", self._zip_code)

    @staticmethod
    def from_dict(d: dict) -> "CostumerAddress":
        return CostumerAddress(
            id=CostumerAddressId(d["id"]),
            user_id=d["user_id"],
            country=d["country"],
            city=d["city"],
            street=d["street"],
            house_number=d["house_number"],
            zip_code=d["zip_code"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": self._user_id,
            "country": self._country,
            "city": self._city,
            "street": self._street,
            "house_number": self._house_number,
            "zip_code": self._zip_code,
        }

    def to_response(self) -> CostumerAddressResponse:
        return CostumerAddressResponse(
            id=str(self.id),
            user_id=self._user_id,
            country=self._country,
            city=self._city,
            street=self._street,
            house_number=self._house_number,
            zip_code=self._zip_code,
        )
