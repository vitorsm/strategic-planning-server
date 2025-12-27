from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.work_record import WorkRecord
from src.services.generic_service import GenericService
from src.services.goal_service import GoalService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.work_record_repository import WorkRecordRepository
from src.services.task_type_service import TaskTypeService
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.work_record_service import WorkRecordService
from src.services.workspace_service import WorkspaceService
from tests.mocks import work_record_mock, FIRST_DEFAULT_ID, user_mock
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestWorkRecordService(GenericEntityServiceTest, TestCase):
    def setUp(self):
        self.work_record_repository = Mock(spec=WorkRecordRepository)
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.task_type_service = Mock(spec=TaskTypeService)
        self.user_service = Mock(spec=UserService)
        self.goal_service = Mock(spec=GoalService)
        self.team_service = Mock(spec=TeamService)

        self.service = WorkRecordService(self.work_record_repository, self.authentication_repository,
                                         self.workspace_service, self.user_service, self.goal_service,
                                         self.team_service, self.task_type_service)

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> WorkRecord:
        return work_record_mock.get_default_work_record()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.work_record_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_update_work_record_invalid_parameters(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.users = [user_mock.get_default_user()]
        updated_entity.name = "new name"

        self.task_type_service.find_by_id.side_effect = EntityNotFoundException("TaskType", str(FIRST_DEFAULT_ID))
        self.goal_service.find_by_id.side_effect = EntityNotFoundException("Goal", str(FIRST_DEFAULT_ID))
        self.team_service.find_by_id.side_effect = EntityNotFoundException("Team", str(FIRST_DEFAULT_ID))
        self.user_service.find_by_id.side_effect = EntityNotFoundException("User", str(FIRST_DEFAULT_ID))

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn("users", str(ex.exception))
        self.assertIn("goal", str(ex.exception))
        self.assertIn("team", str(ex.exception))
        self.assertIn("task_type", str(ex.exception))
