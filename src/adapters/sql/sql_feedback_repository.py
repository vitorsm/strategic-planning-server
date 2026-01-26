from typing import List
from uuid import UUID

from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.feedback_db import FeedbackDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.feedback import Feedback
from src.services.ports.feedback_repository import FeedbackRepository


class SQLFeedbackRepository(SQLRepository[Feedback, FeedbackDB], FeedbackRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def find_by_user_id(self, user_id: UUID) -> List[Feedback]:
        session = self.get_session()
        feedbacks_db = session.query(FeedbackDB).filter(FeedbackDB.user_to == user_id).all()
        return [feedback_db.to_entity() for feedback_db in feedbacks_db]
