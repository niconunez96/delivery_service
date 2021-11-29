from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from .events import ShipmentCreated, ShipmentDelivered, ShipmentMoved
from .shipment_response import ShipmentResponse
from .shipment_status import (
    DELIVERED,
    ON_TRIP,
    PREPARING,
    ShipmentStatus,
    is_valid_status_transition,
)


class ShipmentId:
    _id: UUID

    def __init__(self, id: Optional[UUID] = None):
        self._id = id or uuid4()

    def __str__(self):
        return str(self._id)

    @staticmethod
    def from_string(id: str) -> "ShipmentId":
        return ShipmentId(UUID(id))


class ShipmentDestination:
    country: str
    city: str
    street: str
    house_number: str
    zip_code: int

    def __init__(
        self,
        country: str,
        city: str,
        street: str,
        house_number: str,
        zip_code: int,
    ):
        self.country = country
        self.city = city
        self.street = street
        self.house_number = house_number
        self.zip_code = zip_code

    def to_dict(self) -> dict:
        return {
            "country": self.country,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            "zip_code": self.zip_code,
        }

    @staticmethod
    def from_dict(data: dict) -> "ShipmentDestination":
        return ShipmentDestination(
            country=data["country"],
            city=data["city"],
            street=data["street"],
            house_number=data["house_number"],
            zip_code=data["zip_code"],
        )


class Shipment:
    id: ShipmentId
    _status: ShipmentStatus
    _user_id: str
    _order_id: str
    _destination: ShipmentDestination

    def __init__(
        self,
        id: ShipmentId,
        user_id: str,
        order_id: str,
        destination: ShipmentDestination,
        status: Optional[ShipmentStatus] = None,
    ):
        self.id = id
        self._user_id = user_id
        self._order_id = order_id
        self._destination = destination
        self._status = status or PREPARING

    @staticmethod
    def from_dict(data: dict) -> "Shipment":
        return Shipment(
            ShipmentId.from_string(data["id"]),
            data["user_id"],
            data["order_id"],
            ShipmentDestination.from_dict(data["destination"]),
            data["status"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "status": self._status,
            "user_id": self._user_id,
            "order_id": self._order_id,
            "destination": self._destination.to_dict(),
        }

    def to_response(self) -> ShipmentResponse:
        return ShipmentResponse(
            id=str(self.id),
            status=self._status,
        )

    def created_event(self) -> ShipmentCreated:
        return ShipmentCreated(str(self.id), datetime.utcnow())

    def moved_event(self, country: str, city: str, address: str) -> ShipmentMoved:
        return ShipmentMoved(
            str(self.id),
            datetime.utcnow(),
            country,
            city,
            address,
        )

    def delivered_event(self) -> ShipmentDelivered:
        return ShipmentDelivered(str(self.id), datetime.utcnow())

    def on_trip(self) -> None:
        if not is_valid_status_transition(self._status, ON_TRIP):
            raise ValueError(f"Cannot set status ON_TRIP from status {self._status}")
        self._status = ON_TRIP

    def deliver(self) -> None:
        if not is_valid_status_transition(self._status, DELIVERED):
            raise ValueError(f"Cannot set status DELIVERED from status {self._status}")
        self._status = DELIVERED
