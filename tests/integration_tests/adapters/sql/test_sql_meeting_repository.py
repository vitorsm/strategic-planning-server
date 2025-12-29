from datetime import timedelta
from typing import List

from src.adapters.sql.sql_meeting_repository import SQLMeetingRepository
from src.entities.meeting import Meeting
from src.services.ports.generic_entity_repository import GenericEntityRepository
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import meeting_mock, SECOND_DEFAULT_ID, workspace_mock, user_mock, DEFAULT_CREATED_AT


class TestSQLMeetingRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLMeetingRepository(self.db_instance)

    def compare_entities_custom(self, meeting1: Meeting, meeting2: Meeting) -> bool:
        self.assertEqual(meeting1.meeting_date, meeting2.meeting_date)
        self.assertEqual(meeting1.users, meeting2.users)
        self.assertEqual(meeting1.notes, meeting2.notes)

    def get_repository(self) -> GenericEntityRepository:
        return self.repository

    def get_all_entities(self) -> List[Meeting]:
        meeting1 = self.get_default_entity()
        meeting2 = self.get_default_entity()

        meeting2.id = SECOND_DEFAULT_ID
        meeting2.name = "Meeting 2"
        meeting2.meeting_date = DEFAULT_CREATED_AT + timedelta(days=11)
        meeting2.users = []
        meeting2.notes = []

        return [meeting1, meeting2]

    def get_valid_entity(self) -> Meeting:
        return meeting_mock.get_valid_meeting(workspace=workspace_mock.get_default_workspace(),
                                              created_by=user_mock.get_default_user(),
                                              updated_by=user_mock.get_default_user(),
                                              users=[user_mock.get_default_user()])

    def get_default_entity(self) -> Meeting:
        return meeting_mock.get_default_meeting()

    def get_updated_entity(self) -> Meeting:
        meeting = self.get_default_entity()
        meeting.name = "new name"
        meeting.notes = ["Updated note 1", "Updated note 2", "Updated note 3"]
        return meeting

