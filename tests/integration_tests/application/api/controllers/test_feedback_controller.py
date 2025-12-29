from typing import List
from uuid import uuid4

from src.application.api.mappers.feedback_mapper import FeedbackMapper
from src.entities.feedback import FeedbackType
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import \
    GenericEntityControllerTests
from tests.mocks import SECOND_DEFAULT_ID, feedback_mock, user_mock, workspace_mock


class TestFeedbackController(BaseAPITest, GenericEntityControllerTests):
    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Feedback 2"
        dto2["delivered"] = False
        dto2["description"] = None
        dto2["type"] = FeedbackType.CONSTRUCTIVE.name

        return [dto1, dto2]

    def compare_generic_entities(self, feedback1: dict, feedback2: dict, compare_id: bool = False):
        self.assertEqual(feedback1["delivered"], feedback2["delivered"])
        self.assertEqual(feedback1["user_from"]["id"], feedback2["user_from"]["id"])
        self.assertEqual(feedback1["user_to"]["id"], feedback2["user_to"]["id"])
        self.assertEqual(feedback1["type"], feedback2["type"])
        self.assertEqual(feedback1["description"], feedback2["description"])

    def get_valid_entity(self) -> dict:
        feedback = feedback_mock.get_valid_feedback(
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            workspace=workspace_mock.get_default_workspace(),
            user_from=user_mock.get_default_user(),
            user_to=user_mock.get_default_user(),
        )

        return FeedbackMapper.to_dto(feedback)

    def get_default_entity(self) -> dict:
        return FeedbackMapper.to_dto(feedback_mock.get_default_feedback())

    def get_changed_entity(self) -> dict:
        feedback = self.get_default_entity()
        feedback["delivered"] = False
        feedback["description"] = "new description"
        feedback["type"] = FeedbackType.CONSTRUCTIVE.name
        feedback["description"] = "new description"
        return feedback

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()
        dto3 = self.get_default_entity()

        dto1["name"] = ""
        dto2["user_from"] = {"id": None}
        dto3["user_to"] = {"id": str(uuid4())}

        return [dto1, dto2]

    def get_api_name(self) -> str:
        return "feedbacks"
