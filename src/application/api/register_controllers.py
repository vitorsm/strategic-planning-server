
from flask import Flask
from flask_jwt_extended import JWTManager
from injector import Injector

from src.application.api.controllers.authentication_controller import AuthenticationController
from src.application.api.controllers.feedback_controller import FeedbackController
from src.application.api.controllers.goal_controller import GoalController
from src.application.api.controllers.task_type_controller import TaskTypeController
from src.application.api.controllers.team_controller import TeamController
from src.application.api.controllers.workspace_controller import WorkspaceController
from src.application.api.errors import exception_handler
from src.application.api.controllers.user_controller import UserController


def instantiate_controllers(app: Flask, app_injector: Injector):
    jwt_manager = JWTManager(app)
    controllers = []

    authentication_controller = AuthenticationController(app_injector)
    controllers.append(authentication_controller.controller)

    user_controller = UserController(app_injector)
    controllers.append(user_controller.controller)

    workspace_controller = WorkspaceController(app_injector)
    controllers.append(workspace_controller.controller)

    task_type_controller = TaskTypeController(app_injector)
    controllers.append(task_type_controller.controller)

    team_controller = TeamController(app_injector)
    controllers.append(team_controller.controller)

    feedback_controller = FeedbackController(app_injector)
    controllers.append(feedback_controller.controller)

    goal_controller = GoalController(app_injector)
    controllers.append(goal_controller.controller)

    exception_handler.error_handlers(controllers)
    for controller in controllers:
        app.register_blueprint(controller)
