from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.strategic_plan_db import StrategicPlanDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.strategic_plan import StrategicPlan
from src.services.ports.strategic_plan_repository import StrategicPlanRepository


class SQLStrategicPlanRepository(SQLRepository[StrategicPlan, StrategicPlanDB], StrategicPlanRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

