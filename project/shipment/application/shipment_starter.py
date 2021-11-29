from dataclasses import dataclass
from typing import Optional

from project.costumer_address.application.costumer_address_finder import \
    CostumerAddressFinder
from project.shared.domain.errors import EntityNotFound
from project.shared.domain.event_bus import EventBus
from project.shared.infrastructure.rabbitmq_event_bus import RabbitMQEventBus

from ..domain.shipment import Shipment, ShipmentDestination, ShipmentId
from ..domain.shipment_repo import ShipmentRepo

from ..infrastructure.shipment_mongo_repo import ShipmentMongoRepo

@dataclass(frozen=True)
class ShipmentInfo:
    order_id: str
    user_id: str


class ShipmentStarter:
    _shipment_repo: ShipmentRepo
    _event_bus: EventBus
    _costumer_address_finder: CostumerAddressFinder

    def __init__(
        self,
        shipment_repo: Optional[ShipmentRepo] = None,
        event_bus: Optional[EventBus] = None,
        costumer_address_finder: Optional[CostumerAddressFinder] = None,
    ):
        self._shipment_repo = shipment_repo or ShipmentMongoRepo()
        self._event_bus = event_bus or RabbitMQEventBus()
        self._costumer_address_finder = (
            costumer_address_finder or CostumerAddressFinder()
        )

    def start_shipment(self, shipment_id: ShipmentId, info: ShipmentInfo) -> None:
        try:
            costumer_address = self._costumer_address_finder.find_by_user_id(
                info.user_id)
        except EntityNotFound:
            print("The current user does not have an address")
            return
        shipment_destination = ShipmentDestination(
            costumer_address.country,
            costumer_address.city,
            costumer_address.street,
            costumer_address.house_number,
            costumer_address.zip_code,
        )
        shipment = Shipment(
            shipment_id, info.user_id, info.order_id, shipment_destination
        )
        self._shipment_repo.store(shipment)
        self._event_bus.publish(shipment.created_event())
