import abc
from typing import List
from uuid import UUID

from src.entities.goal import Goal
from src.services.ports.generic_entity_repository import GenericEntityRepository


class GoalRepository(GenericEntityRepository[Goal], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_team_id(self, team_id: UUID) -> List[Goal]:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_user_id(self, user_id: UUID) -> List[Goal]:
        raise NotImplementedError
