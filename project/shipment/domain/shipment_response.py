from dataclasses import dataclass


@dataclass(frozen=True)
class ShipmentResponse:
    id: str
    status: str
