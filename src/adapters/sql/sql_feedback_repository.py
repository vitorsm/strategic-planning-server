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
