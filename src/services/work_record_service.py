from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.work_record import WorkRecord
from src.services.generic_entity_service import GenericEntityService, Entity
from src.services.goal_service import GoalService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.ports.work_record_repository import WorkRecordRepository
from src.services.task_type_service import TaskTypeService
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class WorkRecordService(GenericEntityService[WorkRecord]):

    def __init__(self, work_record_repository: WorkRecordRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService, user_service: UserService, goal_service: GoalService,
                 team_service: TeamService, task_type_service: TaskTypeService):
        self.__work_record_repository = work_record_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service
        self.__user_service = user_service
        self.__goal_service = goal_service
        self.__team_service = team_service
        self.__task_type_service = task_type_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__work_record_repository

    def pre_persist_custom(self, work_record: WorkRecord, is_create: bool):
        invalid_fields = []

        try:
            work_record.users = [self.__user_service.find_by_id(user.id) for user in (work_record.users or [])]
        except EntityNotFoundException:
            invalid_fields.append("users")

        if work_record.goal:
            try:
                work_record.goal = self.__goal_service.find_by_id(work_record.goal.id)
            except EntityNotFoundException:
                invalid_fields.append("goal")

        if work_record.team:
            try:
                work_record.team = self.__team_service.find_by_id(work_record.team.id)
            except EntityNotFoundException:
                invalid_fields.append("team")

        try:
            work_record.task_type = self.__task_type_service.find_by_id(work_record.task_type.id)
        except EntityNotFoundException:
            invalid_fields.append("task_type")

        if invalid_fields:
            raise InvalidEntityException(self._get_entity_type_name(), invalid_fields)

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository
