from typing import List
from uuid import UUID

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

    def find_by_team_id(self, team_id: UUID) -> List[Goal]:
        session = self.get_session()
        goals_db = session.query(GoalDB).filter(GoalDB.team_id == team_id).all()
        return [goal_db.to_entity() for goal_db in goals_db]

    def find_by_user_id(self, user_id: UUID) -> List[Goal]:
        session = self.get_session()
        goals_db = session.query(GoalDB).filter(GoalDB.user_id == user_id).all()
        return [goal_db.to_entity() for goal_db in goals_db]
