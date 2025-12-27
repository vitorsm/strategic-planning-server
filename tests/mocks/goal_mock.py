import random
from datetime import datetime, timedelta
from typing import Optional

from src.entities.goal import Goal, GoalStatus, GoalType
from src.entities.team import Team
from tests.mocks import user_mock, team_mock, generic_entity_mock, DEFAULT_CREATED_AT

now = datetime.now()


def get_valid_goal(status: GoalStatus = GoalStatus.IN_PROGRESS, description: str = None,
                   gtype: GoalType = GoalType.ORGANIZATIONAL, due_date: datetime = now,
                   user=user_mock.get_valid_user(), team: Optional[Team] = team_mock.get_valid_team(),
                   parent_goal: Goal = None, **kwargs) -> Goal:
    goal = object.__new__(Goal)
    if not kwargs.get("name"):
        kwargs["name"] = generic_entity_mock.random_str("Goal")

    generic_entity_mock.fill_valid_entity(goal, **kwargs)
    goal.status = status
    goal.description = description
    goal.due_date = due_date
    goal.user = user
    goal.team = team
    goal.parent_goal = parent_goal
    goal.type = gtype
    return goal


def get_default_goal() -> Goal:
    goal = object.__new__(Goal)
    generic_entity_mock.fill_default_entity(goal, "Goal 1")
    goal.status = GoalStatus.IN_PROGRESS
    goal.description = "Description 1"
    goal.due_date = DEFAULT_CREATED_AT + timedelta(days=10)
    goal.user = user_mock.get_default_user()
    goal.team = team_mock.get_default_team()
    goal.parent_goal = None
    goal.type = GoalType.ORGANIZATIONAL
    return goal
