import json
from datetime import datetime
from dataclasses import dataclass
from project.shared.domain.event_bus import DomainEvent

@dataclass(frozen=True)
class ShipmentMoved(DomainEvent):
    shipment_id: str
    when: datetime
    country: str
    city: str
    address: str

    DOMAIN_EVENT = "shipment_moved"

    def to_json(self) -> str:
        return json.dumps({
            "shipment_id": self.shipment_id,
            "when": self.when.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "country": self.country,
            "city": self.city,
            "address": self.address,
        })
