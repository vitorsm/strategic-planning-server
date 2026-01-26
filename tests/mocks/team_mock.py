import random
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from src.entities.team import Team
from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import workspace_mock, user_mock, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT, FIRST_DEFAULT_ID, generic_entity_mock

now = datetime.now()


def get_valid_team(tid: UUID = None, name: str = None, workspace: Workspace = workspace_mock.get_valid_workspace(),
                   created_by: User = user_mock.get_valid_user(), updated_by: User = user_mock.get_valid_user(),
                   created_at: datetime = now, updated_at: datetime = now, deleted_at: datetime = None,
                   members: List[User] = None, description: Optional[str] = None) -> Team:
    tid = tid if tid else uuid4()
    if not name:
        name = f"Team {int(random.random() * 1000)}"
    if not members:
        members = []

    return Team(id=tid, name=name, workspace=workspace, created_by=created_by, updated_by=updated_by,
                created_at=created_at, updated_at=updated_at, deleted_at=deleted_at,
                members=members, description=description)


def get_default_team() -> Team:
    return get_valid_team(tid=FIRST_DEFAULT_ID, name="Team 1", created_by=user_mock.get_default_user(),
                          updated_by=user_mock.get_default_user(), created_at=DEFAULT_CREATED_AT,
                          updated_at=DEFAULT_UPDATED_AT, members=[user_mock.get_default_user()],
                          workspace=workspace_mock.get_default_workspace(), description="Description 1")
