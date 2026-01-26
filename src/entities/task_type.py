from dataclasses import dataclass
from typing import List, Optional

from src.entities.generic_entity import GenericEntity


@dataclass
class TaskType(GenericEntity):
    color: str
    icon: str
    parent_type: Optional['TaskType']

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append('name')

        if not self.color:
            invalid_fields.append('color')

        if not self.icon:
            invalid_fields.append('icon')

        return invalid_fields
