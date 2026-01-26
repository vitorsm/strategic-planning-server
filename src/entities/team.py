from dataclasses import dataclass
from typing import List, Optional

from src.entities.generic_entity import GenericEntity
from src.entities.user import User


@dataclass
class Team(GenericEntity):
    members: List[User]
    description: Optional[str]

    def _get_invalid_fields(self) -> List[str]:
        if not self.name:
            return ["name"]

        return []
