from flask import Flask
from injector import Module, Binder, singleton

from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.sql_feedback_repository import SQLFeedbackRepository
from src.adapters.sql.sql_task_type_repository import SQLTaskTypeRepository
from src.adapters.sql.sql_team_repository import SQLTeamRepository
from src.adapters.sql.sql_user_repository import SQLUserRepository
from src.adapters.sql.sql_workspace_repository import SQLWorkspaceRepository
from src.application.api.security.flask_authentication_repository import FlaskAuthenticationRepository
from src.services.feedback_service import FeedbackService
from src.services.task_type_service import TaskTypeService
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.workspace_service import WorkspaceService


class DependencyInjector(Module):
    def __init__(self, app: Flask, db_instance: DBInstance):
        self.app = app
        self.db_instance = db_instance

    def configure(self, binder: Binder):
        user_repository = SQLUserRepository(self.db_instance)
        workspace_repository = SQLWorkspaceRepository(self.db_instance)
        task_type_repository = SQLTaskTypeRepository(self.db_instance)
        team_repository = SQLTeamRepository(self.db_instance)
        feedback_repository = SQLFeedbackRepository(self.db_instance)

        authentication_repository = FlaskAuthenticationRepository(user_repository)
        user_service = UserService(user_repository, authentication_repository)
        workspace_service = WorkspaceService(workspace_repository, authentication_repository, user_service)
        task_type_service = TaskTypeService(task_type_repository, authentication_repository, workspace_service)
        team_service = TeamService(team_repository, authentication_repository, workspace_service, user_service)
        feedback_service = FeedbackService(feedback_repository, authentication_repository, workspace_service,
                                           user_service)

        binder.bind(UserService, to=user_service, scope=singleton)
        binder.bind(WorkspaceService, to=workspace_service, scope=singleton)
        binder.bind(TaskTypeService, to=task_type_service, scope=singleton)
        binder.bind(TeamService, to=team_service, scope=singleton)
        binder.bind(FeedbackService, to=feedback_service, scope=singleton)
