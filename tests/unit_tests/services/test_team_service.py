import unittest
from unittest.mock import Mock
from uuid import uuid4

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.team import Team
from src.services.generic_service import GenericService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.team_repository import TeamRepository
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import team_mock, user_mock
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestTeamService(GenericEntityServiceTest, unittest.TestCase):

    def setUp(self):
        self.team_repository = Mock(spec=TeamRepository)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.user_service = Mock(spec=UserService)

        self.service = TeamService(self.team_repository, self.authentication_repository, self.workspace_service,
                                   self.user_service)

        self.user_service.find_by_id.return_value = user_mock.get_default_user()

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> Team:
        return team_mock.get_default_team()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.team_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_update_team_invalid_users(self):
        # given
        new_user_id = uuid4()
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"
        updated_entity.members_ids = [new_user_id]
        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", str(new_user_id))

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn("members", str(ex.exception))
