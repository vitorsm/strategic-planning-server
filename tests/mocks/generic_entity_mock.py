import random
from datetime import datetime
from uuid import UUID, uuid4

from src.entities.generic_entity import GenericEntity
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import user_mock, workspace_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT

now = datetime.now()


def fill_valid_entity(generic_entity: GenericEntity, eid: UUID = None, name: str = None,
                      created_by: User = user_mock.get_valid_user(), updated_by: User = user_mock.get_valid_user(),
                      created_at: datetime = now, updated_at: datetime = now, deleted_at: datetime = None,
                      workspace: Workspace = workspace_mock.get_valid_workspace()):

    eid = eid if eid else uuid4()

    generic_entity.id = eid
    generic_entity.name = name
    generic_entity.created_by = created_by
    generic_entity.updated_by = updated_by
    generic_entity.created_at = created_at
    generic_entity.updated_at = updated_at
    generic_entity.deleted_at = deleted_at
    generic_entity.workspace = workspace


def fill_default_entity(generic_entity: GenericEntity, name: str):
    user = user_mock.get_default_user()
    fill_valid_entity(generic_entity, name=name, eid=FIRST_DEFAULT_ID, created_by=user, updated_by=user,
                      created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT,
                      workspace=workspace_mock.get_default_workspace())


def random_str(prefix: str) -> str:
    return f"{prefix} {int(random.random() * 1000)}"
