from datetime import datetime
from typing import Any, List

from src.adapters.sql.sql_goal_repository import SQLGoalRepository
from src.entities.goal import Goal, GoalStatus, GoalType
from src.services.ports.generic_entity_repository import GenericEntityRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import SECOND_DEFAULT_ID, FIRST_DEFAULT_ID, goal_mock, user_mock, workspace_mock, team_mock


class TestSQLGoalRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):
    def setUp(self):
        super().setUp()
        self.repository = SQLGoalRepository(self.db_instance)

    def compare_entities_custom(self, goal1: Goal, goal2: Goal) -> bool:
        self.assertEqual(goal1.team, goal2.team)
        self.assertEqual(goal1.user, goal2.user)
        self.assertEqual(goal1.status, goal2.status)
        self.assertEqual(goal1.description, goal2.description)
        self.assertEqual(goal1.type, goal2.type)
        self.assertEqual(goal1.due_date, goal2.due_date)
        if goal1.parent_goal:
            self.assertIsNotNone(goal2.parent_goal)
            self.assertEqual(goal1.parent_goal.id, goal2.parent_goal.id)
        else:
            self.assertIsNone(goal2.parent_goal)

    def get_repository(self) -> GenericEntityRepository:
        return self.repository

    def get_all_entities(self) -> List[Goal]:
        goal1 = self.get_default_entity()
        goal2 = self.get_default_entity()

        goal2.id = SECOND_DEFAULT_ID
        goal2.name = "Goal 2"
        goal2.user = None
        goal2.status = GoalStatus.DONE
        goal2.type = GoalType.PERSONAL
        goal2.parent_goal = self.get_default_entity()
        goal2.description = None

        return [goal1, goal2]

    def get_valid_entity(self) -> Goal:
        goal = goal_mock.get_valid_goal()

        goal.created_by = user_mock.get_default_user()
        goal.updated_by = user_mock.get_default_user()
        goal.workspace = workspace_mock.get_default_workspace()
        goal.user = user_mock.get_default_user()
        goal.team = team_mock.get_default_team()

        return goal

    def get_default_entity(self) -> Any:
        return goal_mock.get_default_goal()

    def get_updated_entity(self) -> Any:
        goal = self.get_default_entity()
        goal.name = "new name"
        goal.user = None
        goal.type = GoalType.ORGANIZATIONAL
        goal.status = GoalStatus.DONE
        goal.due_date = datetime.now()
        return goal
