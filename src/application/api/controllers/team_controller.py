from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controllers.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.goal_mapper import GoalMapper
from src.application.api.mappers.reminder_mapper import ReminderMapper
from src.application.api.mappers.team_mapper import TeamMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.goal_service import GoalService
from src.services.reminder_service import ReminderService
from src.services.team_service import TeamService


class TeamController(GenericEntityController[TeamService, TeamMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = self.instantiate_controller()
        self.start_controller()

    def create_custom_endpoints(self):
        @self.controller.route("<string:team_id>/goals", methods=["GET"])
        @jwt_required()
        def get_goals_by_team(team_id: str):
            team_uuid = uuid_mapper.to_uuid(team_id)

            if not team_uuid:
                raise InvalidEntityException("UUID", ["team_id"])

            goal_service = self.app_injector.get(GoalService)
            goals = goal_service.find_by_team(team_uuid)

            return jsonify(GoalMapper.to_dtos(goals)), 200

        @self.controller.route("<string:team_id>/reminders", methods=["GET"])
        @jwt_required()
        def get_reminders_by_team(team_id: str):
            team_uuid = uuid_mapper.to_uuid(team_id)

            if not team_uuid:
                raise InvalidEntityException("UUID", ["team_id"])

            reminder_service = self.app_injector.get(ReminderService)
            reminders = reminder_service.find_by_team(team_uuid)
            dtos = [ReminderMapper.to_dto(reminder) for reminder in reminders]

            return jsonify(dtos), 200

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def get_controller_name(self) -> str:
        return "teams"
