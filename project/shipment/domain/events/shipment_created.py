import json
from datetime import datetime
from dataclasses import dataclass
from project.shared.event_bus import DomainEvent


@dataclass(frozen=True)
class ShipmentCreated(DomainEvent):
    shipment_id: str
    when: datetime
    DOMAIN_EVENT = "shipment_created"

    def to_json(self) -> str:
        return json.dumps(
            {
                "shipment_id": self.shipment_id,
                "when": self.when.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            }
        )
