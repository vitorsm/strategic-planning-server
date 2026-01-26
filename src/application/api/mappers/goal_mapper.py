from typing import List

from src.application.api.mappers.generic_mapper import GenericMapper
from src.entities.goal import Goal
from src.utils import tree_entities_utils


class GoalMapper(GenericMapper[Goal]):

    @classmethod
    def to_dtos(cls, goals: List[Goal]) -> List[dict]:
        if not goals:
            return []

        dtos = [cls.to_dto(goal) for goal in goals]
        return tree_entities_utils.build_tree(dtos, parent_parameter="parent_goal")
