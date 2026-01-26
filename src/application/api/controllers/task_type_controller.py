from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controllers.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.task_type_mapper import TaskTypeMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.task_type_service import TaskTypeService


class TaskTypeController(GenericEntityController[TaskTypeService, TaskTypeMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def put_find_all(self) -> bool:
        return False

    def create_custom_endpoints(self):
        @self.get_controller().route("", methods=["GET"])
        @jwt_required()
        def find_all():
            workspace_id = uuid_mapper.to_uuid(request.args.get("workspace_id"))

            if not workspace_id:
                raise InvalidEntityException("UUID", ["workspace_id"])

            task_type_service = self.app_injector.get(TaskTypeService)
            task_types = task_type_service.find_all(workspace_id)

            return jsonify(TaskTypeMapper.to_dtos(task_types))

    def get_controller_name(self) -> str:
        return "task-types"
