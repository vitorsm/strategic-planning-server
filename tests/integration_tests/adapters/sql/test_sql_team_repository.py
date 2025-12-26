from typing import List

from src.adapters.sql.sql_team_repository import SQLTeamRepository
from src.entities.team import Team
from src.services.ports.generic_entity_repository import GenericEntityRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import team_mock, SECOND_DEFAULT_ID, workspace_mock, user_mock


class TestSQLTeamRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLTeamRepository(self.db_instance)

    def compare_entities_custom(self, team1: Team, team2: Team) -> bool:
        self.assertEqual(team1.members_ids, team2.members_ids)

    def get_repository(self) -> GenericEntityRepository:
        return self.repository

    def get_all_entities(self) -> List[Team]:
        team1 = self.get_default_entity()
        team2 = self.get_default_entity()

        team2.id = SECOND_DEFAULT_ID
        team2.name = "Team 2"
        team2.members_ids = []

        return [team1, team2]

    def get_valid_entity(self) -> Team:
        return team_mock.get_valid_team(workspace=workspace_mock.get_default_workspace(),
                                        created_by=user_mock.get_default_user(),
                                        updated_by=user_mock.get_default_user())

    def get_default_entity(self) -> Team:
        return team_mock.get_default_team()

    def get_updated_entity(self) -> Team:
        team = self.get_default_entity()
        team.name = "new name"
        team.members_ids = [SECOND_DEFAULT_ID]
        return team