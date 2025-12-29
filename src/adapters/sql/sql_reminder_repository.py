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

