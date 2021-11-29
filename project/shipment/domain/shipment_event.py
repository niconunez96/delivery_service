from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from .shipment_status import DELIVERED, ON_TRIP, PREPARING, ShipmentStatus


@dataclass(frozen=True)
class ShipmentEventResponse:
    id: str
    when: datetime
    shipment_id: str
    status: str
    location: dict


class ShipmentEventId:
    _id: UUID

    def __init__(self, id: Optional[UUID] = None):
        self._id = id or uuid4()

    def __str__(self):
        return str(self._id)


@dataclass(frozen=True)
class ShipmentLocation:
    country: str
    city: str
    address: str


@dataclass(frozen=True)
class ShipmentEvent:
    id: ShipmentEventId
    _when: datetime
    _shipment_id: str
    _status: ShipmentStatus
    _location: ShipmentLocation

    @staticmethod
    def from_dict(d: dict):
        return ShipmentEvent(
            ShipmentEventId(d["id"]),
            datetime.strptime(d["when"], "%Y-%m-%dT%H:%M:%S.%f"),
            d["shipment_id"],
            d["status"],
            ShipmentLocation(
                d["location"]["country"],
                d["location"]["city"],
                d["location"]["address"],
            ),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "when": self._when.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "shipment_id": self._shipment_id,
            "status": str(self._status),
            "location": {
                "country": self._location.country,
                "city": self._location.city,
                "address": self._location.address,
            },
        }

    def to_response(self) -> ShipmentEventResponse:
        return ShipmentEventResponse(
            str(self.id),
            self._when,
            self._shipment_id,
            str(self._status),
            {
                "country": self._location.country,
                "city": self._location.city,
                "address": self._location.address,
            },
        )

    @staticmethod
    def create_shipment_preparing(
        shipment_id: str,
        when: datetime,
    ) -> "ShipmentEvent":
        return ShipmentEvent(
            ShipmentEventId(),
            when,
            shipment_id,
            PREPARING,
            ShipmentLocation("", "", ""),
        )

    @staticmethod
    def create_shipment_on_trip(
        shipment_id: str,
        when: datetime,
        country: str,
        city: str,
        address: str,
    ) -> "ShipmentEvent":
        return ShipmentEvent(
            ShipmentEventId(),
            when,
            shipment_id,
            ON_TRIP,
            ShipmentLocation(country, city, address),
        )

    @staticmethod
    def create_shipment_delivered(
        shipment_id: str,
        when: datetime,
    ) -> "ShipmentEvent":
        return ShipmentEvent(
            ShipmentEventId(),
            when,
            shipment_id,
            DELIVERED,
            ShipmentLocation("", "", ""),
        )
