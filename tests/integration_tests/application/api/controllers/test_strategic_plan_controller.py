from datetime import timedelta
from typing import List
from uuid import uuid4

from src.application.api.mappers.strategic_plan_mapper import StrategicPlanMapper
from src.utils import date_utils
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import (
    GenericEntityControllerTests,
)
from tests.mocks import (
    DEFAULT_CREATED_AT,
    FIRST_DEFAULT_ID,
    SECOND_DEFAULT_ID,
    goal_mock,
    strategic_plan_mock,
    task_type_mock,
    user_mock,
    workspace_mock,
)
from src.entities.strategic_plan import TaskTypePlan


class TestStrategicPlanController(BaseAPITest, GenericEntityControllerTests):
    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Strategic Plan 2"
        dto2["start_date"] = date_utils.datetime_to_iso(DEFAULT_CREATED_AT + timedelta(days=11))
        dto2["end_date"] = date_utils.datetime_to_iso(DEFAULT_CREATED_AT + timedelta(days=21))
        dto2["task_type_plans"] = [
            {"task_type": {"id": str(FIRST_DEFAULT_ID)}, "percentage": 20.0}
        ]
        dto2["goals"] = []

        return [dto1, dto2]

    def compare_generic_entities(self, plan1: dict, plan2: dict, compare_id: bool = False):
        self.assertEqual(plan1["start_date"], plan2["start_date"])
        self.assertEqual(plan1["end_date"], plan2["end_date"])

        self.assertEqual(len(plan1["task_type_plans"]), len(plan2["task_type_plans"]))
        for ttp1, ttp2 in zip(plan1["task_type_plans"], plan2["task_type_plans"]):
            self.assertEqual(ttp1["percentage"], ttp2["percentage"])
            self.assertEqual(ttp1["task_type"]["id"], ttp2["task_type"]["id"])

        self.assertEqual(len(plan1["goals"]), len(plan2["goals"]))
        for goal1, goal2 in zip(plan1["goals"], plan2["goals"]):
            self.assertEqual(goal1["id"], goal2["id"])

    def get_valid_entity(self) -> dict:
        plan = strategic_plan_mock.get_valid_strategic_plan(
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            workspace=workspace_mock.get_default_workspace(),
            task_type_plans=[TaskTypePlan(task_type=task_type_mock.get_default_task_type(), percentage=10.0)],
            goals=[goal_mock.get_default_goal()],
        )
        return StrategicPlanMapper.to_dto(plan)

    def get_default_entity(self) -> dict:
        return StrategicPlanMapper.to_dto(strategic_plan_mock.get_default_strategic_plan())

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["end_date"] = date_utils.datetime_to_iso(DEFAULT_CREATED_AT + timedelta(days=30))
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()
        dto3 = self.get_default_entity()

        dto1["name"] = ""
        dto2["task_type_plans"] = [{"task_type": {"id": str(uuid4())}, "percentage": 10.0}]
        dto3["goals"] = [{"id": str(uuid4())}]

        return [dto1, dto2, dto3]

    def get_api_name(self) -> str:
        return "strategic-plans"


