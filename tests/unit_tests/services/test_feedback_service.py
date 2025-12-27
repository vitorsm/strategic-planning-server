from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.feedback import Feedback
from src.services.feedback_service import FeedbackService
from src.services.generic_service import GenericService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.feedback_repository import FeedbackRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import feedback_mock, user_mock, FIRST_DEFAULT_ID
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestFeedbackService(GenericEntityServiceTest, TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.feedback_repository = Mock(spec=FeedbackRepository)
        self.user_service = Mock(spec=UserService)

        self.service = FeedbackService(self.feedback_repository, self.authentication_repository, self.workspace_service,
                                       self.user_service)

        self.user_service.find_by_id.return_value = user_mock.get_default_user()

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> Feedback:
        return feedback_mock.get_default_feedback()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.feedback_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_update_feedback_invalid_user(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"

        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", str(FIRST_DEFAULT_ID))

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn("user_to", str(ex.exception))
        self.assertIn("user_from", str(ex.exception))
