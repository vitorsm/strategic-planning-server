import abc
from typing import List
from uuid import UUID

from src.entities.feedback import Feedback
from src.services.ports.generic_entity_repository import GenericEntityRepository


class FeedbackRepository(GenericEntityRepository[Feedback], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_user_id(self, user_id: UUID) -> List[Feedback]:
        raise NotImplementedError
