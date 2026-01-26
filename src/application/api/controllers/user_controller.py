from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controllers.generic_controller import GenericController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.feedback_mapper import FeedbackMapper
from src.application.api.mappers.goal_mapper import GoalMapper
from src.application.api.mappers.reminder_mapper import ReminderMapper
from src.application.api.mappers.user_mapper import UserMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.feedback_service import FeedbackService
from src.services.goal_service import GoalService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.reminder_service import ReminderService
from src.services.user_service import UserService


class UserController(GenericController[UserService, UserMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def get_controller_name(self) -> str:
        return "users"

    def has_create_endpoint(self) -> bool:
        return False

    def create_endpoints(self):

        @self.controller.route("", methods=["POST"])
        def create_user():
            user_dto = request.get_json()
            user = UserMapper.to_entity(user_dto)

            if not user:
                raise InvalidEntityException("", ["invalid entity"])

            user_service = self.app_injector.get(UserService)
            user_service.create(user)

            return jsonify(UserMapper.to_dto(user)), 201

        @self.controller.route("me", methods=["GET"])
        @jwt_required()
        def get_current_user():
            authentication_repository = self.app_injector.get(AuthenticationRepository)
            current_user = authentication_repository.get_current_user()
            return jsonify(UserMapper.to_dto(current_user)), 200

        @self.controller.route("login/<string:login>", methods=["GET"])
        @jwt_required()
        def get_user_by_login(login: str):
            user_service = self.app_injector.get(UserService)
            user = user_service.find_by_login(login)
            return jsonify(UserMapper.to_dto(user)), 200

        @self.controller.route("<string:user_id>/reminders", methods=["GET"])
        @jwt_required()
        def get_reminders_by_user(user_id: str):
            user_uuid = uuid_mapper.to_uuid(user_id)

            if not user_uuid:
                raise InvalidEntityException("UUID", ["user_id"])

            reminder_service = self.app_injector.get(ReminderService)
            reminders = reminder_service.find_by_user(user_uuid)
            dtos = [ReminderMapper.to_dto(reminder) for reminder in reminders]

            return jsonify(dtos), 200

        @self.controller.route("<string:user_id>/goals", methods=["GET"])
        @jwt_required()
        def get_goals_by_user(user_id: str):
            user_uuid = uuid_mapper.to_uuid(user_id)

            if not user_uuid:
                raise InvalidEntityException("UUID", ["user_id"])

            goal_service = self.app_injector.get(GoalService)
            goals = goal_service.find_by_user(user_uuid)
            dtos = [GoalMapper.to_dto(goal) for goal in goals]

            return jsonify(dtos), 200

        @self.controller.route("<string:user_id>/feedbacks", methods=["GET"])
        @jwt_required()
        def get_feedbacks_by_user(user_id: str):
            user_uuid = uuid_mapper.to_uuid(user_id)

            if not user_uuid:
                raise InvalidEntityException("UUID", ["user_id"])

            feedback_service = self.app_injector.get(FeedbackService)
            feedbacks = feedback_service.find_by_user(user_uuid)
            dtos = [FeedbackMapper.to_dto(feedback) for feedback in feedbacks]

            return jsonify(dtos), 200
