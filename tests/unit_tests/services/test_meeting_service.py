from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.generic_service import GenericService
from src.services.meeting_service import MeetingService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.meeting_repository import MeetingRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import meeting_mock, FIRST_DEFAULT_ID
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestMeetingService(GenericEntityServiceTest, TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.user_service = Mock(spec=UserService)
        self.meeting_repository = Mock(spec=MeetingRepository)
        self.service = MeetingService(self.meeting_repository, self.workspace_service, self.authentication_repository,
                                      self.user_service)
        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> Any:
        return meeting_mock.get_default_meeting()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.meeting_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_update_meeting_invalid_parameters(self):
        # given
        updated_entity = self.get_default_entity()

        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", str(FIRST_DEFAULT_ID))

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn("users", str(ex.exception))
