from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.team import Team
from src.services.generic_entity_service import GenericEntityService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.team_repository import TeamRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class TeamService(GenericEntityService[Team]):

    def __init__(self, team_repository: TeamRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService, user_service: UserService):
        self.__team_repository = team_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service
        self.__user_service = user_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> TeamRepository:
        return self.__team_repository

    def pre_persist_custom(self, team: Team, is_create: bool):
        try:
            [self.__user_service.find_by_id(user_id) for user_id in team.members_ids]
        except EntityNotFoundException:
            raise InvalidEntityException(self._get_entity_type_name(), ["members"])

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository
