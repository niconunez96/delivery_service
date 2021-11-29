from dataclasses import dataclass


@dataclass
class CostumerAddressInfo:
    user_id: str
    country: str
    city: str
    street: str
    house_number: str
    zip_code: int

    @staticmethod
    def from_dict(data: dict):
        return CostumerAddressInfo(
            user_id=data["user_id"],
            country=data["country"],
            city=data["city"],
            street=data["street"],
            house_number=data["house_number"],
            zip_code=data["zip_code"],
        )

    def to_dict(self) -> dict:
        return {
            "country": self.country,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            "zip_code": self.zip_code,
        }
