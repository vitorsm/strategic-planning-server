from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.team_db import TeamDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.team import Team
from src.services.ports.team_repository import TeamRepository


class SQLTeamRepository(SQLRepository[Team, TeamDB], TeamRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
