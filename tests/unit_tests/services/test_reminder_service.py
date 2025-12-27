from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.generic_service import GenericService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.reminder_repository import ReminderRepository
from src.services.reminder_service import ReminderService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import reminder_mock, user_mock, FIRST_DEFAULT_ID
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestReminderService(GenericEntityServiceTest, TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.user_service = Mock(spec=UserService)
        self.reminder_repository = Mock(spec=ReminderRepository)

        self.service = ReminderService(self.reminder_repository, self.authentication_repository,
                                       self.workspace_service, self.user_service)

        self.user_service.find_by_id.return_value = user_mock.get_default_user()

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> Any:
        return reminder_mock.get_default_reminder()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.reminder_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_reminder_entity_without_permission(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"
        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", str(FIRST_DEFAULT_ID))

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn("to_user", str(ex.exception))