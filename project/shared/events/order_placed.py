import json
from dataclasses import dataclass

from ..event_bus import DomainEvent


@dataclass
class OrderPlaced(DomainEvent):
    order_id: str
    user_id: str

    DOMAIN_EVENT = "order_placed"

    def to_json(self):
        return json.dumps({"order_id": self.order_id, "user_id": self.user_id})
