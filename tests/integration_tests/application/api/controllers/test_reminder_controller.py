from typing import List
from uuid import uuid4

from src.application.api.mappers.reminder_mapper import ReminderMapper
from src.entities.reminder import ReminderStatus
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import (
    GenericEntityControllerTests,
)
from tests.mocks import (
    FIRST_DEFAULT_ID,
    SECOND_DEFAULT_ID,
    reminder_mock,
    user_mock,
    workspace_mock,
)


class TestReminderController(BaseAPITest, GenericEntityControllerTests):
    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Reminder 2"
        dto2["status"] = ReminderStatus.DONE.value
        dto2["description"] = None
        dto2["related_user"] = None
        dto2["related_team"] = None

        return [dto1, dto2]

    def compare_generic_entities(self, reminder1: dict, reminder2: dict, compare_id: bool = False):
        self.assertEqual(reminder1["description"], reminder2["description"])
        self.assertEqual(reminder1["status"], reminder2["status"])
        self.assertEqual(reminder1["to_user"]["id"], reminder2["to_user"]["id"])

        if reminder1.get("related_user"):
            self.assertIsNotNone(reminder2.get("related_user"))
            self.assertEqual(reminder1.get("related_user").get("id"), reminder2.get("related_user").get("id"))
        else:
            self.assertIsNone(reminder2.get("related_user"))

        if reminder1.get("related_team"):
            self.assertIsNotNone(reminder2.get("related_team"))
            self.assertEqual(reminder1.get("related_team").get("id"), reminder2.get("related_team").get("id"))
        else:
            self.assertIsNone(reminder2.get("related_team"))

    def get_valid_entity(self) -> dict:
        reminder = reminder_mock.get_valid_reminder(
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            workspace=workspace_mock.get_default_workspace(),
            to_user=user_mock.get_default_user(),
        )
        return ReminderMapper.to_dto(reminder)

    def get_default_entity(self) -> dict:
        return ReminderMapper.to_dto(reminder_mock.get_default_reminder())

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["description"] = "new description"
        dto["status"] = ReminderStatus.DONE.value
        dto["to_user"]["id"] = str(SECOND_DEFAULT_ID)
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto1["name"] = ""
        dto2["to_user"] = {"id": str(uuid4())}

        return [dto1, dto2]

    def get_api_name(self) -> str:
        return "reminders"
