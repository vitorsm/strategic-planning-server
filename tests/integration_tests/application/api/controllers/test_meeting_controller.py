from datetime import timedelta
from typing import List
from uuid import uuid4

from src.application.api.mappers.meeting_mapper import MeetingMapper
from src.utils import date_utils
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import (
    GenericEntityControllerTests,
)
from tests.mocks import (
    DEFAULT_CREATED_AT,
    FIRST_DEFAULT_ID,
    SECOND_DEFAULT_ID,
    meeting_mock,
    user_mock,
    workspace_mock,
)


class TestMeetingController(BaseAPITest, GenericEntityControllerTests):
    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Meeting 2"
        dto2["meeting_date"] = date_utils.datetime_to_iso(DEFAULT_CREATED_AT + timedelta(days=11))
        dto2["users"] = []
        dto2["notes"] = []

        return [dto1, dto2]

    def compare_generic_entities(self, meeting1: dict, meeting2: dict, compare_id: bool = False):
        self.assertEqual(meeting1["meeting_date"], meeting2["meeting_date"])
        self.assertEqual(meeting1["notes"], meeting2["notes"])

        self.assertEqual(len(meeting1["users"]), len(meeting2["users"]))
        for user1, user2 in zip(meeting1["users"], meeting2["users"]):
            self.assertEqual(user1["id"], user2["id"])
            self.assertEqual(user1["name"], user2["name"])
            self.assertEqual(user1["login"], user2["login"])
            self.assertIsNone(user2["password"])

    def get_valid_entity(self) -> dict:
        meeting = meeting_mock.get_valid_meeting(
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            workspace=workspace_mock.get_default_workspace(),
            users=[user_mock.get_default_user()]
        )
        return MeetingMapper.to_dto(meeting)

    def get_default_entity(self) -> dict:
        return MeetingMapper.to_dto(meeting_mock.get_default_meeting())

    def get_changed_entity(self) -> dict:
        meeting = self.get_default_entity()
        meeting["name"] = "Meeting 1 Updated"
        meeting["meeting_date"] = date_utils.datetime_to_iso(DEFAULT_CREATED_AT + timedelta(days=30))
        meeting["notes"] = ["Note 1", "Note 2", "Note 3"]
        return meeting

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()
        dto3 = self.get_default_entity()

        dto1["name"] = ""
        dto2["users"] = []
        dto3["users"] = [{"id": str(uuid4())}]

        return [dto1, dto2, dto3]

    def get_api_name(self) -> str:
        return "meetings"


