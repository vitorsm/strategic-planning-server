from typing import List
from uuid import uuid4

from src.application.api.mappers.work_record_mapper import WorkRecordMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import (
    GenericEntityControllerTests,
)
from tests.mocks import (
    FIRST_DEFAULT_ID,
    SECOND_DEFAULT_ID,
    goal_mock,
    task_type_mock,
    team_mock,
    user_mock,
    work_record_mock,
    workspace_mock,
)


class TestWorkRecordController(BaseAPITest, GenericEntityControllerTests):
    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Work Record 2"
        dto2["description"] = None
        dto2["goal"] = None
        dto2["team"] = None
        dto2["users"] = []

        return [dto1, dto2]

    def compare_generic_entities(self, record1: dict, record2: dict, compare_id: bool = False):
        self.assertEqual(record1["description"], record2["description"])
        self.assertEqual(record1["task_type"]["id"], record2["task_type"]["id"])

        if record1.get("goal"):
            self.assertEqual(record1["goal"]["id"], record2["goal"]["id"])
        else:
            self.assertIsNone(record2.get("goal"))

        if record1.get("team"):
            self.assertEqual(record1["team"]["id"], record2["team"]["id"])
        else:
            self.assertIsNone(record2.get("team"))

        self.assertEqual(len(record1["users"]), len(record2["users"]))
        for user1, user2 in zip(record1["users"], record2["users"]):
            self.assertEqual(user1["id"], user2["id"])
            self.assertEqual(user1["name"], user2["name"])
            self.assertEqual(user1["login"], user2["login"])
            self.assertIsNone(user2["password"])

    def get_valid_entity(self) -> dict:
        record = work_record_mock.get_valid_work_record(
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            workspace=workspace_mock.get_default_workspace(),
            task_type=task_type_mock.get_default_task_type(),
            users=[user_mock.get_default_user()],
            goal=goal_mock.get_default_goal(),
            team=team_mock.get_default_team(),
        )
        return WorkRecordMapper.to_dto(record)

    def get_default_entity(self) -> dict:
        return WorkRecordMapper.to_dto(work_record_mock.get_default_work_record())

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["description"] = "new description"
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()
        dto3 = self.get_default_entity()

        dto1["name"] = ""
        dto2["task_type"] = {"id": str(uuid4())}
        dto3["users"] = [{"id": str(uuid4())}]

        return [dto1, dto2, dto3]

    def get_api_name(self) -> str:
        return "work-records"
