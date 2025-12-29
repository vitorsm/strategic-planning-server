from datetime import timedelta
from typing import Any, List

from src.adapters.sql.sql_strategic_plan_repository import SQLStrategicPlanRepository
from src.entities.strategic_plan import StrategicPlan, TaskTypePlan
from src.services.ports.generic_entity_repository import GenericEntityRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import SECOND_DEFAULT_ID, strategic_plan_mock, user_mock, workspace_mock, task_type_mock, goal_mock, \
    DEFAULT_CREATED_AT


class TestSQLStrategicPlanRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):
    def setUp(self):
        super().setUp()
        self.repository = SQLStrategicPlanRepository(self.db_instance)

    def compare_entities_custom(self, plan1: StrategicPlan, plan2: StrategicPlan) -> bool:
        self.assertEqual(plan1.start_date, plan2.start_date)
        self.assertEqual(plan1.end_date, plan2.end_date)
        self.assertEqual(len(plan1.task_type_plans), len(plan2.task_type_plans))
        self.assertEqual(len(plan1.goals), len(plan2.goals))

        for ttp1, ttp2 in zip(plan1.task_type_plans, plan2.task_type_plans):
            self.assertEqual(ttp1.task_type.id, ttp2.task_type.id)
            self.assertEqual(ttp1.percentage, ttp2.percentage)

        for goal1, goal2 in zip(plan1.goals, plan2.goals):
            self.assertEqual(goal1.id, goal2.id)

    def get_repository(self) -> GenericEntityRepository:
        return self.repository

    def get_all_entities(self) -> List[StrategicPlan]:
        plan1 = self.get_default_entity()
        plan2 = self.get_default_entity()

        plan2.id = SECOND_DEFAULT_ID
        plan2.name = "Strategic Plan 2"
        plan2.start_date = DEFAULT_CREATED_AT + timedelta(days=11)
        plan2.end_date = DEFAULT_CREATED_AT + timedelta(days=21)
        plan2.task_type_plans = [TaskTypePlan(task_type=task_type_mock.get_default_task_type(), percentage=20.0)]
        plan2.goals = []

        return [plan1, plan2]

    def get_valid_entity(self) -> StrategicPlan:
        plan = strategic_plan_mock.get_valid_strategic_plan()

        plan.created_by = user_mock.get_default_user()
        plan.updated_by = user_mock.get_default_user()
        plan.workspace = workspace_mock.get_default_workspace()
        plan.task_type_plans = [TaskTypePlan(task_type=task_type_mock.get_default_task_type(), percentage=15.0)]
        plan.goals = [goal_mock.get_default_goal()]

        return plan

    def get_default_entity(self) -> Any:
        plan = strategic_plan_mock.get_default_strategic_plan()
        plan.task_type_plans = [TaskTypePlan(task_type=task_type_mock.get_default_task_type(), percentage=10.0)]
        plan.goals = [goal_mock.get_default_goal()]
        return plan

    def get_updated_entity(self) -> Any:
        plan = self.get_default_entity()
        plan.name = "new name"
        plan.start_date = DEFAULT_CREATED_AT + timedelta(days=15)
        plan.end_date = DEFAULT_CREATED_AT + timedelta(days=25)
        return plan

