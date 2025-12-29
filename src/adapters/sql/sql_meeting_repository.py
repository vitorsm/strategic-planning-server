from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.meeting_db import MeetingDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.meeting import Meeting
from src.services.ports.meeting_repository import MeetingRepository


class SQLMeetingRepository(SQLRepository[Meeting, MeetingDB], MeetingRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

