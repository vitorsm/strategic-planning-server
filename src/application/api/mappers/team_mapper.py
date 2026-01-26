from typing import Union, Optional, List

from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.generic_entity import GenericEntity
from src.entities.team import Team


class TeamMapper(GenericMapper[Team]):

    @classmethod
    def to_dto(cls, entity: GenericEntity) -> Union[Optional[dict], List[dict]]:
        if not isinstance(entity, Team):
            return super().to_dto(entity)

        dto = super().to_dto(entity)
        dto["number_of_members"] = len(entity.members) if entity.members else 0

        return dto
