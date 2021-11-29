class DomainEvent:
    DOMAIN_EVENT = ""

    def to_json(self) -> str:
        raise NotImplementedError


class EventBus:
    def publish(self, event: DomainEvent) -> None:
        raise NotImplementedError()
