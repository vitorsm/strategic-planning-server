from dataclasses import dataclass
from typing import List, Optional

from src.entities.generic_entity import GenericEntity
from src.entities.goal import Goal
from src.entities.task_type import TaskType
from src.entities.team import Team
from src.entities.user import User


@dataclass
class WorkRecord(GenericEntity):
    task_type: TaskType
    users: List[User]
    goal: Optional[Goal]
    team: Optional[Team]
    description: Optional[str]

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")

        if not self.task_type:
            invalid_fields.append("task_type")

        return invalid_fields
