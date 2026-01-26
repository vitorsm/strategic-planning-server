from flask import Flask
from injector import Module, Binder, singleton

from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.sql_feedback_repository import SQLFeedbackRepository
from src.adapters.sql.sql_goal_repository import SQLGoalRepository
from src.adapters.sql.sql_meeting_repository import SQLMeetingRepository
from src.adapters.sql.sql_reminder_repository import SQLReminderRepository
from src.adapters.sql.sql_strategic_plan_repository import SQLStrategicPlanRepository
from src.adapters.sql.sql_task_type_repository import SQLTaskTypeRepository
from src.adapters.sql.sql_team_repository import SQLTeamRepository
from src.adapters.sql.sql_user_repository import SQLUserRepository
from src.adapters.sql.sql_work_record_repository import SQLWorkRecordRepository
from src.adapters.sql.sql_workspace_repository import SQLWorkspaceRepository
from src.application.api.security.flask_authentication_repository import FlaskAuthenticationRepository
from src.services.feedback_service import FeedbackService
from src.services.goal_service import GoalService
from src.services.meeting_service import MeetingService
from src.services.ports.authentication_repository import AuthenticationRepository
from src.services.reminder_service import ReminderService
from src.services.strategic_plan_service import StrategicPlanService
from src.services.task_type_service import TaskTypeService
from src.services.team_service import TeamService
from src.services.user_service import UserService
from src.services.work_record_service import WorkRecordService
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
        goal_repository = SQLGoalRepository(self.db_instance)
        meeting_repository = SQLMeetingRepository(self.db_instance)
        reminder_repository = SQLReminderRepository(self.db_instance)
        strategic_plan_repository = SQLStrategicPlanRepository(self.db_instance)
        work_record_repository = SQLWorkRecordRepository(self.db_instance)

        authentication_repository = FlaskAuthenticationRepository(user_repository)
        user_service = UserService(user_repository, authentication_repository)
        workspace_service = WorkspaceService(workspace_repository, authentication_repository, user_service)
        task_type_service = TaskTypeService(task_type_repository, authentication_repository, workspace_service)
        team_service = TeamService(team_repository, authentication_repository, workspace_service, user_service)
        feedback_service = FeedbackService(feedback_repository, authentication_repository, workspace_service,
                                           user_service)
        goal_service = GoalService(goal_repository, authentication_repository, workspace_service, user_service,
                                   team_service)
        meeting_service = MeetingService(meeting_repository, workspace_service, authentication_repository, user_service)
        reminder_service = ReminderService(reminder_repository, authentication_repository, workspace_service,
                                           user_service, team_service)
        strategic_plan_service = StrategicPlanService(strategic_plan_repository, workspace_service,
                                                      authentication_repository, task_type_service, goal_service)
        work_record_service = WorkRecordService(work_record_repository, authentication_repository, workspace_service,
                                                user_service, goal_service, team_service, task_type_service)

        binder.bind(AuthenticationRepository, to=authentication_repository, scope=singleton)
        binder.bind(UserService, to=user_service, scope=singleton)
        binder.bind(WorkspaceService, to=workspace_service, scope=singleton)
        binder.bind(TaskTypeService, to=task_type_service, scope=singleton)
        binder.bind(TeamService, to=team_service, scope=singleton)
        binder.bind(FeedbackService, to=feedback_service, scope=singleton)
        binder.bind(GoalService, to=goal_service, scope=singleton)
        binder.bind(MeetingService, to=meeting_service, scope=singleton)
        binder.bind(ReminderService, to=reminder_service, scope=singleton)
        binder.bind(StrategicPlanService, to=strategic_plan_service, scope=singleton)
        binder.bind(WorkRecordService, to=work_record_service, scope=singleton)
