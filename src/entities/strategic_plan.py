from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.entities.generic_entity import GenericEntity
from src.entities.goal import Goal
from src.entities.task_type import TaskType


@dataclass
class TaskTypePlan:
    task_type: TaskType
    percentage: float


@dataclass
class StrategicPlan(GenericEntity):
    task_type_plans: List[TaskTypePlan]
    goals: List[Goal]
    start_date: datetime
    end_date: datetime

    def _get_invalid_fields(self) -> List[str]:
        invalid_fields = []

        if not self.name:
            invalid_fields.append("name")
        if not self.start_date:
            invalid_fields.append("start_date")
        if not self.end_date:
            invalid_fields.append("end_date")
            
        return invalid_fields