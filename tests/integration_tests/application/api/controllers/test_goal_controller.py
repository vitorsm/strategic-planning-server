from typing import List
from uuid import uuid4

from src.application.api.mappers.goal_mapper import GoalMapper
from src.application.api.mappers.user_mapper import UserMapper
from src.entities.goal import GoalStatus, GoalType
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import \
    GenericEntityControllerTests
from tests.mocks import SECOND_DEFAULT_ID, FIRST_DEFAULT_ID, goal_mock, user_mock, workspace_mock, team_mock


class TestGoalController(BaseAPITest, GenericEntityControllerTests):
    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Goal 2"
        dto2["status"] = GoalStatus.DONE.name
        dto2["description"] = None
        dto2["type"] = GoalType.PERSONAL.name
        dto2["user"] = None
        dto2["parent_goal_id"] = str(FIRST_DEFAULT_ID)

        return [dto1, dto2]

    def compare_generic_entities(self, goal1: dict, goal2: dict, compare_id: bool = False):
        self.assertEqual(goal1["status"], goal2["status"])
        self.assertEqual(goal1["description"], goal2["description"])
        self.assertEqual(goal1["type"], goal2["type"])
        self.assertEqual(goal1["due_date"], goal2["due_date"])
        self.assertEqual(goal1["parent_goal_id"], goal2["parent_goal_id"])

        if goal1.get("user"):
            self.assertEqual(goal1["user"]["id"], goal2["user"]["id"])
        else:
            self.assertIsNone(goal2.get("user"))

        if goal1.get("team"):
            self.assertEqual(goal1["team"]["id"], goal2["team"]["id"])
        else:
            self.assertIsNone(goal2.get("team"))

    def get_valid_entity(self) -> dict:
        goal = goal_mock.get_valid_goal(
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            workspace=workspace_mock.get_default_workspace(),
            user=user_mock.get_default_user(),
            team=team_mock.get_default_team(),
        )

        return GoalMapper.to_dto(goal)

    def get_default_entity(self) -> dict:
        return GoalMapper.to_dto(goal_mock.get_default_goal())

    def get_changed_entity(self) -> dict:
        goal = self.get_default_entity()
        goal["status"] = GoalStatus.DONE.name
        goal["description"] = "new description"
        goal["type"] = GoalType.PERSONAL.name
        return goal

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()
        dto3 = self.get_default_entity()

        dto1["name"] = ""
        dto2["user"] = {"id": str(uuid4())}
        dto3["type"] = None

        return [dto1, dto2, dto3]

    def get_api_name(self) -> str:
        return "goals"
