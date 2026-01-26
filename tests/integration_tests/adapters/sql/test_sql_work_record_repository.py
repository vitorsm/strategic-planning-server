from typing import List

from src.adapters.sql.sql_work_record_repository import SQLWorkRecordRepository
from src.entities.work_record import WorkRecord
from src.services.ports.generic_entity_repository import GenericEntityRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import work_record_mock, SECOND_DEFAULT_ID, workspace_mock, user_mock, task_type_mock, goal_mock, \
    team_mock


class TestSQLWorkRecordRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLWorkRecordRepository(self.db_instance)

    def compare_entities_custom(self, work_record1: WorkRecord, work_record2: WorkRecord) -> bool:
        self.assertEqual(work_record1.description, work_record2.description)
        self.assertEqual(work_record1.task_type, work_record2.task_type)
        self.assertEqual(work_record1.team, work_record2.team)
        self.assertEqual(work_record1.users, work_record2.users)
        if work_record1.goal:
            self.assertIsNotNone(work_record2.goal)
            self.assertEqual(work_record1.goal.id, work_record2.goal.id)
        else:
            self.assertIsNone(work_record2.goal)

    def get_repository(self) -> GenericEntityRepository:
        return self.repository

    def get_all_entities(self) -> List[WorkRecord]:
        work_record1 = self.get_default_entity()
        work_record2 = self.get_default_entity()

        work_record2.id = SECOND_DEFAULT_ID
        work_record2.name = "Work Record 2"
        work_record2.description = None
        work_record2.goal = None
        work_record2.team = None
        work_record2.users = []

        return [work_record1, work_record2]

    def get_valid_entity(self) -> WorkRecord:
        return work_record_mock.get_valid_work_record(
            workspace=workspace_mock.get_default_workspace(),
            created_by=user_mock.get_default_user(),
            updated_by=user_mock.get_default_user(),
            task_type=task_type_mock.get_default_task_type(),
            goal=goal_mock.get_default_goal(),
            team=team_mock.get_default_team(),
            users=[user_mock.get_default_user()]
        )

    def get_default_entity(self) -> WorkRecord:
        return work_record_mock.get_default_work_record()

    def get_updated_entity(self) -> WorkRecord:
        work_record = self.get_default_entity()
        work_record.name = "new name"
        work_record.description = "updated description"
        work_record.goal = None
        work_record.team = None
        work_record.users.append(user_mock.get_valid_user(uid=SECOND_DEFAULT_ID))
        return work_record

