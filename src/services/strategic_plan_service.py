from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.strategic_plan import StrategicPlan
from src.services.generic_entity_service import GenericEntityService
from src.services.goal_service import GoalService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.ports.generic_entity_repository import GenericEntityRepository
from src.services.ports.strategic_plan_repository import StrategicPlanRepository
from src.services.task_type_service import TaskTypeService
from src.services.workspace_service import WorkspaceService


class StrategicPlanService(GenericEntityService[StrategicPlan]):
    def __init__(self, strategic_plan_repository: StrategicPlanRepository, workspace_service: WorkspaceService,
                 authentication_repository: AuthenticationRepository, task_type_service: TaskTypeService,
                 goal_service: GoalService):
        self.__strategic_plan_repository = strategic_plan_repository
        self.__workspace_service = workspace_service
        self.__authentication_repository = authentication_repository
        self.__task_type_service = task_type_service
        self.__goal_service = goal_service

    def get_workspace_service(self) -> WorkspaceService:
        return self.__workspace_service

    def get_repository(self) -> GenericEntityRepository:
        return self.__strategic_plan_repository

    def pre_persist_custom(self, strategic_plan: StrategicPlan, is_create: bool):
        invalid_fields = []

        try:
            self.__fill_task_types_plans(strategic_plan)
        except EntityNotFoundException:
            invalid_fields.append("task_type_plans")

        try:
            if strategic_plan.goals:
                strategic_plan.goals = [self.__goal_service.find_by_id(goal.id) for goal in strategic_plan.goals]
        except EntityNotFoundException:
            invalid_fields.append("goals")

        if invalid_fields:
            raise InvalidEntityException(self._get_entity_type_name(), invalid_fields)

    def __fill_task_types_plans(self, strategic_plan: StrategicPlan):
        if not strategic_plan.task_type_plans:
            return

        for task_type_plan in strategic_plan.task_type_plans:
            task_type_plan.task_type = self.__task_type_service.find_by_id(task_type_plan.task_type.id)


    def get_authentication_repository(self) -> AuthenticationRepository:
        return self.__authentication_repository
