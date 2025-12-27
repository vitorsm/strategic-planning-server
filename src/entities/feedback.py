from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from src.entities.generic_entity import GenericEntity
from src.entities.user import User


class FeedbackType(Enum):
    POSITIVE = 1
    CONSTRUCTIVE = 2


@dataclass
class Feedback(GenericEntity):
    description: Optional[str]
    type: FeedbackType
    user_from: User
    user_to: User
    delivered: bool

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")
        if not self.type:
            invalid_fields.append("type")
        if not self.user_from:
            invalid_fields.append("user_from")
        if not self.user_to:
            invalid_fields.append("user_to")

        return invalid_fields
