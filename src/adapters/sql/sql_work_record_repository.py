from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.work_record_db import WorkRecordDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.work_record import WorkRecord
from src.services.ports.work_record_repository import WorkRecordRepository


class SQLWorkRecordRepository(SQLRepository[WorkRecord, WorkRecordDB], WorkRecordRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

