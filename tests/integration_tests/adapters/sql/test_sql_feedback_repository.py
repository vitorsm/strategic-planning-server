import unittest
from typing import Any, List

from src.adapters.sql.sql_feedback_repository import SQLFeedbackRepository
from src.entities.feedback import Feedback, FeedbackType
from tests.integration_tests.adapters.base_sql_alchemy_test import BaseSQLAlchemyTest
from tests.integration_tests.adapters.sql.generic_entity_repository_test import GenericEntityRepositoryTest
from tests.mocks import feedback_mock, SECOND_DEFAULT_ID, user_mock, workspace_mock


class TestSQLFeedbackRepository(BaseSQLAlchemyTest, GenericEntityRepositoryTest):

    def setUp(self):
        super().setUp()
        self.repository = SQLFeedbackRepository(self.db_instance)

    def compare_entities_custom(self, feedback1: Feedback, feedback2: Feedback):
        self.assertEqual(feedback1.user_from, feedback2.user_from)
        self.assertEqual(feedback1.user_to, feedback2.user_to)
        self.assertEqual(feedback1.delivered, feedback2.delivered)
        self.assertEqual(feedback1.description, feedback2.description)
        self.assertEqual(feedback1.type, feedback2.type)

    def get_repository(self) -> SQLFeedbackRepository:
        return self.repository

    def get_all_entities(self) -> List[Feedback]:
        feedback1 = feedback_mock.get_default_feedback()
        feedback2 = feedback_mock.get_default_feedback()

        feedback2.id = SECOND_DEFAULT_ID
        feedback2.name = "Feedback 2"
        feedback2.description = None
        feedback2.delivered = False
        feedback2.type = FeedbackType.CONSTRUCTIVE

        return [feedback1, feedback2]

    def get_valid_entity(self) -> Feedback:
        feedback = feedback_mock.get_valid_feedback()

        feedback.created_by = user_mock.get_default_user()
        feedback.updated_by = user_mock.get_default_user()
        feedback.user_from = user_mock.get_default_user()
        feedback.user_to = user_mock.get_default_user()
        feedback.workspace = workspace_mock.get_default_workspace()

        return feedback

    def get_default_entity(self) -> Feedback:
        return feedback_mock.get_default_feedback()

    def get_updated_entity(self) -> Any:
        feedback = feedback_mock.get_default_feedback()
        feedback.name = "new name"
        feedback.delivered = False
        feedback.type = FeedbackType.CONSTRUCTIVE
        return feedback
