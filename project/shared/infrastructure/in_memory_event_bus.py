from typing import List

from .event_bus import DomainEvent, EventBus


class InMemoryEventBus(EventBus):
    events: List[DomainEvent] = []

    def publish(self, event: DomainEvent) -> None:
        self.events.append(event)
