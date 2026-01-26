from typing import List
from uuid import UUID

from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.reminder_db import ReminderDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.reminder import Reminder
from src.services.ports.reminder_repository import ReminderRepository


class SQLReminderRepository(SQLRepository[Reminder, ReminderDB], ReminderRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def find_by_team_id(self, team_id: UUID) -> List[Reminder]:
        session = self.get_session()
        reminders_db = session.query(ReminderDB).filter(ReminderDB.related_team_id == team_id).all()
        return [reminder_db.to_entity() for reminder_db in reminders_db]

    def find_by_user_id(self, user_id: UUID) -> List[Reminder]:
        session = self.get_session()
        reminders_db = session.query(ReminderDB).filter(ReminderDB.related_user_id == user_id).all()
        return [reminder_db.to_entity() for reminder_db in reminders_db]
