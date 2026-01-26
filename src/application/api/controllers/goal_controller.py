from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controllers.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.goal_mapper import GoalMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.goal_service import GoalService


class GoalController(GenericEntityController[GoalService, GoalMapper]):
    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def create_custom_endpoints(self):
        @self.get_controller().route("", methods=["GET"])
        @jwt_required()
        def find_all():
            workspace_id = uuid_mapper.to_uuid(request.args.get("workspace_id"))

            if not workspace_id:
                raise InvalidEntityException("UUID", ["workspace_id"])

            goal_service = self.app_injector.get(GoalService)
            goals = goal_service.find_all(workspace_id)

            return jsonify(GoalMapper.to_dtos(goals))

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def get_controller_name(self) -> str:
        return "goals"

    def put_find_all(self) -> bool:
        return False

