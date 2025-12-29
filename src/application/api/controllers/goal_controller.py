from flask import Blueprint
from injector import Injector

from src.application.api.controllers.generic_entity_controller import GenericEntityController
from src.application.api.mappers.goal_mapper import GoalMapper
from src.services.goal_service import GoalService


class GoalController(GenericEntityController[GoalService, GoalMapper]):
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
        return "goals"

