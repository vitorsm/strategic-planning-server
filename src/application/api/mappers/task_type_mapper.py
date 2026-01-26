from typing import List

from src.application.api.mappers.generic_mapper import GenericMapper
from src.entities.task_type import TaskType
from src.utils import tree_entities_utils


class TaskTypeMapper(GenericMapper[TaskType]):
    @classmethod
    def to_dtos(cls, task_types: List[TaskType]) -> List[dict]:
        if not task_types:
            return []

        dtos = [cls.to_dto(tt) for tt in task_types]
        return tree_entities_utils.build_tree(dtos, parent_parameter="parent_type")
