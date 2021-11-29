from typing import Optional
from uuid import UUID, uuid4


class CostumerAddressId:
    _id: UUID

    def __init__(self, id: Optional[UUID] = None):
        self._id = id or uuid4()

    def __str__(self):
        return str(self._id)

    @staticmethod
    def from_string(id: str):
        return CostumerAddressId(UUID(id))
