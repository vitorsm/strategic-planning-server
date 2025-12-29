from flask import Blueprint
from injector import Injector

from src.application.api.controllers.generic_entity_controller import GenericEntityController
from src.application.api.mappers.strategic_plan_mapper import StrategicPlanMapper
from src.services.strategic_plan_service import StrategicPlanService


class StrategicPlanController(GenericEntityController[StrategicPlanService, StrategicPlanMapper]):
    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def create_custom_endpoints(self):
        pass

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def get_controller_name(self) -> str:
        return "strategic-plans"


