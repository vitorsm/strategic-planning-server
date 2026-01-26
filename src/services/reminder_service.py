from typing import List
from uuid import UUID

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.reminder import Reminder
from src.services.generic_entity_service import GenericEntityService, Entity
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.ports.reminder_repository import ReminderRepository
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class ReminderService(GenericEntityService[Reminder]):
    def __init__(self, reminder_repository: ReminderRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService, user_service: UserService, team_service: TeamService):
        self.__reminder_repository = reminder_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service
        self.__user_service = user_service
        self.__team_service = team_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__reminder_repository

    def pre_persist_custom(self, reminder: Reminder, is_create: bool):
        invalid_fields = []
        
        try:
            reminder.to_user = self.__user_service.find_by_id(reminder.to_user.id)
        except EntityNotFoundException:
            invalid_fields.append("to_user")
        
        if reminder.related_user:
            try:
                reminder.related_user = self.__user_service.find_by_id(reminder.related_user.id)
            except EntityNotFoundException:
                invalid_fields.append("related_user")
        
        if reminder.related_team:
            try:
                reminder.related_team = self.__team_service.find_by_id(reminder.related_team.id)
            except EntityNotFoundException:
                invalid_fields.append("related_team")
        
        if invalid_fields:
            raise InvalidEntityException(self._get_entity_type_name(), invalid_fields)

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def find_by_team(self, team_id: UUID) -> List[Reminder]:
        team = self.__team_service.find_by_id(team_id)
        return self.__reminder_repository.find_by_team_id(team.id)

    def find_by_user(self, user_id: UUID) -> List[Reminder]:
        user = self.__user_service.find_by_id(user_id)
        return self.__reminder_repository.find_by_user_id(user.id)
