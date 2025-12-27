from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.meeting import Meeting
from src.services.generic_entity_service import GenericEntityService, Entity
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.ports.meeting_repository import MeetingRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class MeetingService(GenericEntityService[Meeting]):

    def __init__(self, meeting_repository: MeetingRepository, workspace_service: WorkspaceService,
                 authentication_repository: AuthenticationRepository, user_service: UserService):
        self.__meeting_repository = meeting_repository
        self.__workspace_service = workspace_service
        self.__authentication_repository = authentication_repository
        self.__user_service = user_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__meeting_repository

    def pre_persist_custom(self, meeting: Meeting, is_create: bool):
        try:
            meeting.users = [self.__user_service.find_by_id(user.id) for user in meeting.users]
        except EntityNotFoundException:
            raise InvalidEntityException(self._get_entity_type_name(), ["users"])

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository
