import random
from datetime import datetime
from uuid import UUID, uuid4

from src.entities.task_type import TaskType
from tests.mocks import workspace_mock, user_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT, \
    generic_entity_mock

now = datetime.now()


def get_valid_task_type(parent_type: TaskType = None, **kwargs) -> TaskType:
    if not kwargs.get("name"):
        kwargs["name"] = f"Task type {int(random.random() * 1000)}"

    task_type = object.__new__(TaskType)
    generic_entity_mock.fill_valid_entity(task_type, **kwargs)
    task_type.parent_type = parent_type
    return task_type


def get_default_task_type() -> TaskType:
    task_type = object.__new__(TaskType)
    generic_entity_mock.fill_default_entity(task_type, name="Type 1")
    task_type.parent_type = None
    return task_type

