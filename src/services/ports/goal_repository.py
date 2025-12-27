import abc

from src.entities.goal import Goal
from src.services.ports.generic_entity_repository import GenericEntityRepository


class GoalRepository(GenericEntityRepository[Goal], metaclass=abc.ABCMeta):
    pass