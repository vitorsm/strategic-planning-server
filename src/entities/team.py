from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.entities.generic_entity import GenericEntity


@dataclass
class Team(GenericEntity):
    members_ids: List[UUID]

    def _get_invalid_fields(self) -> List[str]:
        if not self.name:
            return ["name"]

        return []
