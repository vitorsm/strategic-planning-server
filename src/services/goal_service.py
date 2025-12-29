from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.goal import Goal
from src.services.generic_entity_service import GenericEntityService, Entity
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.ports.goal_repository import GoalRepository
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class GoalService(GenericEntityService[Goal]):
    def __init__(self, goal_repository: GoalRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService, user_service: UserService, team_service: TeamService):
        self.__goal_repository = goal_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service
        self.__user_service = user_service
        self.__team_service = team_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__goal_repository

    def pre_persist_custom(self, goal: Goal, is_create: bool):
        invalid_fields = []
        if goal.user:
            try:
                goal.user = self.__user_service.find_by_id(goal.user.id)
            except EntityNotFoundException:
                invalid_fields.append("user")

        if goal.team:
            try:
                goal.team = self.__team_service.find_by_id(goal.team.id)
            except EntityNotFoundException:
                invalid_fields.append("team")

        if goal.parent_goal_id:
            try:
                goal.parent_goal = self.find_by_id(goal.parent_goal_id)
            except EntityNotFoundException:
                invalid_fields.append("parent_goal_id")

        if invalid_fields:
            raise InvalidEntityException(self._get_entity_type_name(), invalid_fields)

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository
