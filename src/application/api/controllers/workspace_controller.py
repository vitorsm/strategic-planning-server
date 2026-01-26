from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controllers.generic_controller import GenericController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.user_mapper import UserMapper
from src.application.api.mappers.workspace_mapper import WorkspaceMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.workspace_service import WorkspaceService


class WorkspaceController(GenericController[WorkspaceService, WorkspaceMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        @self.get_controller().route("<string:workspace_id>/users", methods=["GET"])
        @jwt_required()
        def get_workspace_users(workspace_id: str):
            uuid_workspace_id = uuid_mapper.to_uuid(workspace_id)

            if not uuid_workspace_id:
                raise InvalidEntityException("UUID", ["uuid"])

            workspace_service = self.app_injector.get(WorkspaceService)
            users = workspace_service.get_workspace_users(uuid_workspace_id)

            return jsonify([UserMapper.to_dto(user) for user in users])

        @self.get_controller().route("<string:workspace_id>/users", methods=["POST"])
        @jwt_required()
        def create_workspace_users(workspace_id: str):
            uuid_workspace_id = uuid_mapper.to_uuid(workspace_id)

            if not uuid_workspace_id:
                raise InvalidEntityException("UUID", ["uuid"])

            user_dto = request.get_json()
            user = UserMapper.to_entity(user_dto)

            workspace_service = self.app_injector.get(WorkspaceService)
            user = workspace_service.create_workspace_user(user, uuid_workspace_id)

            return jsonify(UserMapper.to_dto(user))

        @self.get_controller().route("<string:workspace_id>/users/<string:user_id>", methods=["GET"])
        @jwt_required()
        def get_workspace_user(workspace_id: str, user_id: str):
            uuid_workspace_id = uuid_mapper.to_uuid(workspace_id)
            uuid_user_id = uuid_mapper.to_uuid(user_id)

            if not uuid_workspace_id or not uuid_user_id:
                raise InvalidEntityException("UUID", ["uuid"])

            workspace_service = self.app_injector.get(WorkspaceService)
            user = workspace_service.get_workspace_user(uuid_user_id, uuid_workspace_id)

            return jsonify(UserMapper.to_dto(user))

        @self.get_controller().route("<string:workspace_id>/users/<string:user_id>", methods=["PUT"])
        @jwt_required()
        def update_workspace_users(workspace_id: str, user_id: str):
            uuid_workspace_id = uuid_mapper.to_uuid(workspace_id)

            if not uuid_workspace_id:
                raise InvalidEntityException("UUID", ["uuid"])

            user_dto = request.get_json()

            if user_id != user_dto.get("id"):
                raise InvalidEntityException("UUID", ["id"])

            user = UserMapper.to_entity(user_dto)

            workspace_service = self.app_injector.get(WorkspaceService)
            user = workspace_service.update_workspace_user(user, uuid_workspace_id)

            return jsonify(UserMapper.to_dto(user))

        @self.get_controller().route("<string:workspace_id>/users/<string:user_id>", methods=["DELETE"])
        @jwt_required()
        def delete_workspace_users(workspace_id: str, user_id: str):
            uuid_workspace_id = uuid_mapper.to_uuid(workspace_id)
            uuid_user_id = uuid_mapper.to_uuid(user_id)

            if not uuid_workspace_id or not uuid_user_id:
                raise InvalidEntityException("UUID", ["uuid"])

            workspace_service = self.app_injector.get(WorkspaceService)
            workspace_service.delete_workspace_user(uuid_user_id, uuid_workspace_id)

            return '', 204

    def get_controller_name(self) -> str:
        return "workspaces"
