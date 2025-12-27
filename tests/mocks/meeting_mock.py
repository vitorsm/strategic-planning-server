import random
from datetime import datetime, timedelta
from typing import List

from src.entities.meeting import Meeting
from src.entities.user import User
from tests.mocks import user_mock, generic_entity_mock, DEFAULT_CREATED_AT

now = datetime.now()


def get_valid_meeting(users: List[User] = None, notes: List[str] = None,
                      meeting_date: datetime = now, **kwargs) -> Meeting:

    if not kwargs.get("name"):
        kwargs["name"] = generic_entity_mock.random_str("Meeting")

    if users is None:
        users = [user_mock.get_valid_user()]
    if notes is None:
        notes = [f"Note {int(random.random() * 1000)}"]

    meeting = object.__new__(Meeting)
    generic_entity_mock.fill_valid_entity(meeting, **kwargs)
    meeting.users = users
    meeting.notes = notes
    meeting.meeting_date = meeting_date

    return meeting


def get_default_meeting() -> Meeting:
    meeting = object.__new__(Meeting)
    generic_entity_mock.fill_default_entity(meeting, name="Meeting 1")
    meeting.users = [user_mock.get_default_user()]
    meeting.notes = ["Note 1", "Note 2"]
    meeting.meeting_date = DEFAULT_CREATED_AT + timedelta(days=10)
    return meeting
