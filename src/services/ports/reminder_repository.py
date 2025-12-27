import abc

from src.entities.reminder import Reminder
from src.services.ports.generic_entity_repository import GenericEntityRepository


class ReminderRepository(GenericEntityRepository[Reminder], metaclass=abc.ABCMeta):
    pass
