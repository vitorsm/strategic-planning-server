from typing import Optional

from src.entities.reminder import Reminder, ReminderStatus
from src.entities.team import Team
from src.entities.user import User
from tests.mocks import user_mock, team_mock, generic_entity_mock


def get_valid_reminder(to_user: User = user_mock.get_valid_user(), description: str = None, 
                      status: ReminderStatus = ReminderStatus.PENDING,
                      related_user: Optional[User] = None, related_team: Optional[Team] = None, **kwargs) -> Reminder:
    if description is None:
        description = generic_entity_mock.random_str("Description")

    if not kwargs.get("name"):
        kwargs["name"] = generic_entity_mock.random_str("Reminder")
        
    reminder = object.__new__(Reminder)

    generic_entity_mock.fill_valid_entity(reminder, **kwargs)

    reminder.to_user = to_user
    reminder.status = status
    reminder.related_user = related_user
    reminder.related_team = related_team
    reminder.description = description
    return reminder


def get_default_reminder() -> Reminder:
    reminder = object.__new__(Reminder)
    generic_entity_mock.fill_default_entity(reminder, name="Reminder 1")
    reminder.to_user = user_mock.get_default_user()
    reminder.status = ReminderStatus.PENDING
    reminder.related_user = user_mock.get_default_user()
    reminder.related_team = team_mock.get_default_team()
    reminder.description = "Description 1"
    return reminder
