import random
from typing import List, Optional

from src.entities.goal import Goal
from src.entities.task_type import TaskType
from src.entities.team import Team
from src.entities.user import User
from src.entities.work_record import WorkRecord
from tests.mocks import task_type_mock, goal_mock, team_mock, generic_entity_mock, user_mock


def get_valid_work_record(task_type: TaskType = task_type_mock.get_valid_task_type(), users: List[User] = None,
                          goal: Optional[Goal] = goal_mock.get_valid_goal(),
                          team: Optional[Team] = team_mock.get_valid_team(),
                          description: Optional[str] = None, **kwargs) -> WorkRecord:
    if not kwargs.get("name"):
        kwargs["name"] = f"Task type {int(random.random() * 1000)}"
        
    work_record = object.__new__(WorkRecord)
    generic_entity_mock.fill_valid_entity(work_record, **kwargs)
    work_record.task_type = task_type
    work_record.users = users if users else [user_mock.get_valid_user()]
    work_record.goal = goal
    work_record.team = team
    work_record.description = description if description is not None else generic_entity_mock.random_str("Descrition")
    return work_record


def get_default_work_record() -> WorkRecord:
    work_record = object.__new__(WorkRecord)
    generic_entity_mock.fill_default_entity(work_record, "Work Record 1")
    work_record.task_type = task_type_mock.get_default_task_type()
    work_record.users = [user_mock.get_default_user()]
    work_record.goal = goal_mock.get_default_goal()
    work_record.team = team_mock.get_default_team()
    work_record.description = "Description 1"
    return work_record
