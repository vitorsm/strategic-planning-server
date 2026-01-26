from typing import List
from uuid import UUID

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.feedback import Feedback
from src.services.generic_entity_service import GenericEntityService, Entity
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.feedback_repository import FeedbackRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class FeedbackService(GenericEntityService[Feedback]):
    def __init__(self, feedback_repository: FeedbackRepository, authentication_repository: AuthenticationRepository,
                 workspace_service: WorkspaceService, user_service: UserService):
        self.__feedback_repository = feedback_repository
        self.__authentication_repository = authentication_repository
        self.__workspace_service = workspace_service
        self.__user_service = user_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__feedback_repository

    def pre_persist_custom(self, feedback: Feedback, is_create: bool):
        invalid_fields = []
        try:
            feedback.user_from = self.__user_service.find_by_id(feedback.user_from.id)
        except EntityNotFoundException:
            invalid_fields.append("user_from")

        try:
            feedback.user_to = self.__user_service.find_by_id(feedback.user_to.id)
        except EntityNotFoundException:
            invalid_fields.append("user_to")

        if invalid_fields:
            raise InvalidEntityException(self._get_entity_type_name(), invalid_fields)

    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository

    def find_by_user(self, user_id: UUID) -> List[Feedback]:
        user = self.__user_service.find_by_id(user_id)
        return self.__feedback_repository.find_by_user_id(user.id)
