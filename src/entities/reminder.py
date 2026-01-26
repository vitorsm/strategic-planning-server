from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from src.entities.generic_entity import GenericEntity
from src.entities.team import Team
from src.entities.user import User


class ReminderStatus(Enum):
    PENDING = "PENDING"
    DONE = "DONE"


@dataclass
class Reminder(GenericEntity):
    to_user: User
    status: ReminderStatus
    related_user: Optional[User]
    related_team: Optional[Team]
    description: Optional[str]


    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.to_user:
            invalid_fields.append("to_user")
        if not self.name:
            invalid_fields.append("name")
        if not self.status:
            invalid_fields.append("status")

        return invalid_fields
