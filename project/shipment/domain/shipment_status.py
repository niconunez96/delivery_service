from typing_extensions import Literal

PREPARING = "PREPARING"
ON_TRIP = "ON_TRIP"
DELIVERED = "DELIVERED"

ShipmentStatus = Literal[PREPARING, ON_TRIP, DELIVERED]


def is_valid_status_transition(
    from_status: ShipmentStatus,
    to_status: ShipmentStatus,
) -> bool:
    valid_transitions = {
        PREPARING: [ON_TRIP],
        ON_TRIP: [DELIVERED, ON_TRIP],
        DELIVERED: [ON_TRIP],
    }
    return (
        valid_transitions.get(from_status)
        and to_status in valid_transitions.get(from_status))
