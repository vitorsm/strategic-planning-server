from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from src.entities.generic_entity import GenericEntity
from src.entities.team import Team
from src.entities.user import User


class GoalType(Enum):
    PERSONAL = 1
    ORGANIZATIONAL = 2


class GoalStatus(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2
    ARCHIVED = 3


@dataclass
class Goal(GenericEntity):
    status: GoalStatus
    description: Optional[str]
    type: GoalType
    due_date: datetime
    user: Optional[User]
    team: Optional[Team]
    parent_goal: Optional['Goal']

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")
        if not self.status:
            invalid_fields.append("status")
        if not self.type:
            invalid_fields.append("type")
        if not self.due_date:
            invalid_fields.append("due_date")
        if not self.user and not self.team:
            invalid_fields.append("user")
            invalid_fields.append("team")

        return invalid_fields
