from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.strategic_plan import StrategicPlan
from src.services.generic_service import GenericService
from src.services.goal_service import GoalService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.strategic_plan_repository import StrategicPlanRepository
from src.services.strategic_plan_service import StrategicPlanService
from src.services.task_type_service import TaskTypeService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService
from tests.mocks import strategic_plan_mock, task_type_mock, goal_mock, FIRST_DEFAULT_ID
from tests.unit_tests.services.generic_entity_service_test import GenericEntityServiceTest


class TestStrategicPlanService(GenericEntityServiceTest, TestCase):
    def setUp(self):
        self.strategic_plan_repository = Mock(spec=StrategicPlanRepository)
        self.authentication_repository = Mock(spec=AuthenticationRepository)
        self.task_type_service = Mock(spec=TaskTypeService)
        self.workspace_service = Mock(spec=WorkspaceService)
        self.goal_service = Mock(spec=GoalService)
        self.service = StrategicPlanService(self.strategic_plan_repository, self.workspace_service,
                                            self.authentication_repository, self.task_type_service,
                                            self.goal_service)

        self.task_type_service.find_by_id.return_value = task_type_mock.get_default_task_type()
        self.goal_service.find_by_id.return_value = goal_mock.get_default_goal()

        super().setUp()

    def get_workspace_service(self) -> Mock:
        return self.workspace_service

    def get_default_entity(self) -> StrategicPlan:
        return strategic_plan_mock.get_default_strategic_plan()

    def get_service(self) -> GenericService:
        return self.service

    def get_repository(self) -> Mock:
        return self.strategic_plan_repository

    def get_authentication_repository(self) -> Mock:
        return self.authentication_repository

    def test_update_strategic_plan_invalid_parameters(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"

        self.task_type_service.find_by_id.side_effect = EntityNotFoundException("TaskType", str(FIRST_DEFAULT_ID))
        self.goal_service.find_by_id.side_effect = EntityNotFoundException("Goal", str(FIRST_DEFAULT_ID))

        # when
        with self.assertRaises(InvalidEntityException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn("task_type_plans", str(ex.exception))
        self.assertIn("goals", str(ex.exception))
