import unittest
from typing import Any, List

from src.adapters.sql.sql_reminder_repository import SQLReminderRepository
from src.entities.reminder import Reminder, ReminderStatus
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import reminder_mock, SECOND_DEFAULT_ID, user_mock, team_mock, workspace_mock


class TestSQLReminderRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLReminderRepository(self.db_instance)

    def compare_entities_custom(self, reminder1: Reminder, reminder2: Reminder):
        self.assertEqual(reminder1.to_user, reminder2.to_user)
        self.assertEqual(reminder1.status, reminder2.status)
        self.assertEqual(reminder1.related_user, reminder2.related_user)
        self.assertEqual(reminder1.related_team, reminder2.related_team)
        self.assertEqual(reminder1.description, reminder2.description)

    def get_repository(self) -> SQLReminderRepository:
        return self.repository

    def get_all_entities(self) -> List[Reminder]:
        reminder1 = reminder_mock.get_default_reminder()
        reminder2 = reminder_mock.get_default_reminder()

        reminder2.id = SECOND_DEFAULT_ID
        reminder2.name = "Reminder 2"
        reminder2.status = ReminderStatus.DONE
        reminder2.description = None
        reminder2.related_user = None
        reminder2.related_team = None

        return [reminder1, reminder2]

    def get_valid_entity(self) -> Reminder:
        reminder = reminder_mock.get_valid_reminder()

        reminder.created_by = user_mock.get_default_user()
        reminder.updated_by = user_mock.get_default_user()
        reminder.to_user = user_mock.get_default_user()
        reminder.workspace = workspace_mock.get_default_workspace()

        return reminder

    def get_default_entity(self) -> Reminder:
        return reminder_mock.get_default_reminder()

    def get_updated_entity(self) -> Any:
        reminder = reminder_mock.get_default_reminder()
        reminder.name = "new name"
        reminder.status = ReminderStatus.DONE
        reminder.description = "new description"
        reminder.related_user = user_mock.get_default_user()
        reminder.related_team = None
        return reminder

