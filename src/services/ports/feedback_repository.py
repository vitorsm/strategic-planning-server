import abc

from src.entities.feedback import Feedback
from src.services.ports.generic_entity_repository import GenericEntityRepository


class FeedbackRepository(GenericEntityRepository[Feedback], metaclass=abc.ABCMeta):
    pass
