import abc

from src.entities.strategic_plan import StrategicPlan
from src.services.ports.generic_entity_repository import GenericEntityRepository


class StrategicPlanRepository(GenericEntityRepository[StrategicPlan], metaclass=abc.ABCMeta):
    pass
