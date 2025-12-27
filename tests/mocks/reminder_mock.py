from src.entities.reminder import Reminder
from src.entities.user import User
from tests.mocks import user_mock, generic_entity_mock


def get_valid_reminder(to_user: User = user_mock.get_valid_user(), description: str = None, **kwargs) -> Reminder:
    if description is None:
        description = generic_entity_mock.random_str("Description")

    reminder = object.__new__(Reminder)
    generic_entity_mock.fill_valid_entity(reminder, **kwargs)
    reminder.to_user = to_user
    reminder.description = description
    return reminder


def get_default_reminder() -> Reminder:
    reminder = object.__new__(Reminder)
    generic_entity_mock.fill_default_entity(reminder, name="Reminder 1")
    reminder.to_user = user_mock.get_default_user()
    reminder.description = "Description 1"
    return reminder
