from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.goal_db import GoalDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.goal import Goal
from src.services.ports.goal_repository import GoalRepository


class SQLGoalRepository(SQLRepository[Goal, GoalDB], GoalRepository):
    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
