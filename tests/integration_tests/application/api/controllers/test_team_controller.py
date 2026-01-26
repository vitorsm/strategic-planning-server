from typing import List
from uuid import uuid4

from src.application.api.mappers.team_mapper import TeamMapper
from src.application.api.mappers.user_mapper import UserMapper
from tests.integration_tests.application.api.base_api_test import BaseAPITest
from tests.integration_tests.application.api.controllers.generic_entity_controller_test import \
    GenericEntityControllerTests
from tests.mocks import team_mock, FIRST_DEFAULT_ID, SECOND_DEFAULT_ID, user_mock


class TestTeamController(BaseAPITest, GenericEntityControllerTests):

    def get_all_entities(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto2["id"] = str(SECOND_DEFAULT_ID)
        dto2["name"] = "Team 2"
        dto2["members"] = []
        dto2["description"] = None

        return [dto1, dto2]

    def compare_generic_entities(self, entity1: dict, entity2: dict, compare_id: bool = False):
        self.assertEqual(entity1.get("description"), entity2.get("description"))
        self.assertEqual(len(entity1["members"]), len(entity2["members"]))

        for member1, member2 in zip(entity1["members"], entity2["members"]):
            self.assertEqual(member1["id"], member2["id"])
            self.assertEqual(member1["name"], member2["name"])
            self.assertEqual(member1["login"], member2["login"])

    def get_valid_entity(self) -> dict:
        default_user_mock = UserMapper.to_dto(user_mock.get_default_user())

        dto = TeamMapper.to_dto(team_mock.get_valid_team())
        dto["workspace"] = {"id": str(FIRST_DEFAULT_ID)}
        dto["created_by"] = default_user_mock
        dto["updated_by"] = default_user_mock
        dto["members"] = [default_user_mock]
        dto["description"] = "Description"

        return dto

    def get_default_entity(self) -> dict:
        return TeamMapper.to_dto(team_mock.get_default_team())

    def get_changed_entity(self) -> dict:
        dto = self.get_default_entity()
        dto["name"] = "new name"
        dto["members"] = [{"id": str(SECOND_DEFAULT_ID), "name": "User 2", "login": "user2"}]
        dto["description"] = "New description"
        return dto

    def get_invalid_entity(self) -> List[dict]:
        dto1 = self.get_default_entity()
        dto2 = self.get_default_entity()

        dto1["name"] = ""
        dto2["members"] = [{"id": str(uuid4())}]

        return [dto1, dto2]

    def get_api_name(self) -> str:
        return "teams"
