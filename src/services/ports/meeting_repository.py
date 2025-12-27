import abc

from src.entities.meeting import Meeting
from src.services.ports.generic_entity_repository import GenericEntityRepository


class MeetingRepository(GenericEntityRepository[Meeting], metaclass=abc.ABCMeta):
    pass
