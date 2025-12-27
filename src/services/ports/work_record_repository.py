import abc

from src.entities.work_record import WorkRecord
from src.services.ports.generic_entity_repository import GenericEntityRepository


class WorkRecordRepository(GenericEntityRepository[WorkRecord], metaclass=abc.ABCMeta):
    pass
