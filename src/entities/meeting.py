from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.entities.generic_entity import GenericEntity
from src.entities.user import User


@dataclass
class Meeting(GenericEntity):
    users: List[User]
    notes: List[str]
    meeting_date: datetime

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")
        if not self.users:
            invalid_fields.append("users")
        if not self.meeting_date:
            invalid_fields.append("meeting_date")

        return invalid_fields
