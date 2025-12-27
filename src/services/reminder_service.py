from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.reminder import Reminder
from src.services.generic_entity_service import GenericEntityService, Entity
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.ports.reminder_repository import ReminderRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class ReminderService(GenericEntityService[Reminder]):
    def __init__(self, reminder_repository: ReminderRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService, user_service: UserService):
        self.__reminder_repository = reminder_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service
        self.__user_service = user_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__reminder_repository

    def pre_persist_custom(self, reminder: Reminder, is_create: bool):
        try:
            reminder.to_user = self.__user_service.find_by_id(reminder.to_user.id)
        except EntityNotFoundException:
            raise InvalidEntityException(self._get_entity_type_name(), ["to_user"])

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository
