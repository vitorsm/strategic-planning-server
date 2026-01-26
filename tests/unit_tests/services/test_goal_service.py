import unittest
from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.goal import Goal
from src.services.generic_service import GenericService
from src.services.goal_service import GoalService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.goal_repository import GoalRepository
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import goal_mock, user_mock, team_mock, FIRST_DEFAULT_ID
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestGoalService(GenericEntityServiceTest, TestCase):
    def setUp(self):
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.goal_repository = Mock(spec=GoalRepository)
        self.user_service = Mock(spec=UserService)
        self.team_service = Mock(spec=TeamService)

        self.service = GoalService(self.goal_repository, self.authentication_repository, self.workspace_service,
                                   self.user_service, self.team_service)

        self.user_service.find_by_id.return_value = user_mock.get_default_user()
        self.team_service.find_by_id.return_value = team_mock.get_default_team()

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> Goal:
        return goal_mock.get_default_goal()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.goal_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_create_goal_invalid_parameters(self):
        # given
        entity = self.get_default_entity()
        entity.parent_goal = goal_mock.get_default_goal()

        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", str(FIRST_DEFAULT_ID))
        self.team_service.find_by_id.side_effect = EntityNotFoundException("Team", str(FIRST_DEFAULT_ID))
        self.goal_repository.find_by_id.return_value = None

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().create(entity)

        # then
        self.get_repository().create.assert_not_called()
        self.assertIn("user", str(ex.exception))
        self.assertIn("team", str(ex.exception))
        self.assertIn("parent_goal", str(ex.exception))
