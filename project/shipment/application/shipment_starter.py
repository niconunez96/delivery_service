from dataclasses import dataclass
from typing import Optional

from project.costumer_address.application.costumer_address_finder import \
    CostumerAddressFinder
from project.shared.errors import EntityNotFound
from project.shared.event_bus import EventBus

from ..domain.shipment import Shipment, ShipmentDestination, ShipmentId
from ..domain.shipment_repo import ShipmentRepo


@dataclass(frozen=True)
class ShipmentInfo:
    user_id: str
    order_id: str


class ShipmentStarter:
    _shipment_repo: ShipmentRepo
    _event_bus: EventBus
    _costumer_address_finder: CostumerAddressFinder

    def __init__(
        self,
        shipment_repo: ShipmentRepo,
        event_bus: EventBus,
        costumer_address_finder: Optional[CostumerAddressFinder] = None,
    ):
        self._shipment_repo = shipment_repo
        self._event_bus = event_bus
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
