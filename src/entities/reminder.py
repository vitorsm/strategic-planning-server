from dataclasses import dataclass
from typing import Optional, List

from src.entities.generic_entity import GenericEntity
from src.entities.user import User


@dataclass
class Reminder(GenericEntity):
    to_user: User
    description: Optional[str]

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.to_user:
            invalid_fields.append("to_user")
        if not self.name:
            invalid_fields.append("name")

        return invalid_fields
