import json
from dataclasses import dataclass
from datetime import datetime

from project.shared.event_bus import DomainEvent


@dataclass(frozen=True)
class ShipmentDelivered(DomainEvent):
    shipment_id: str
    when: datetime

    DOMAIN_EVENT = "shipment_delivered"

    def to_json(self) -> str:
        return json.dumps(
            {
                "shipment_id": self.shipment_id,
                "when": self.when.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            }
        )
