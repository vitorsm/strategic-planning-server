import abc

from src.services.ports.generic_entity_repository import GenericEntityRepository


class TeamRepository(GenericEntityRepository, metaclass=abc.ABCMeta):
    pass
