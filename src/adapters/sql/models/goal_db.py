from sqlalchemy import Column, String, Text, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.goal import Goal, GoalStatus, GoalType
from src.utils import enum_utils


class GoalDB(GenericEntityDB, Base[Goal]):
    __tablename__ = 'goal'

    status = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    feedback_type = Column(String(100), nullable=False)
    due_date = Column(DateTime, nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=True)
    team_id = Column(ForeignKey("team.id"), nullable=True)
    parent_goal_id = Column(ForeignKey("goal.id"), nullable=True)

    user_db = relationship("UserDB", foreign_keys="GoalDB.user_id", lazy="joined")
    team_db = relationship("TeamDB", foreign_keys="GoalDB.team_id", lazy="joined")

    def __init__(self, goal: Goal):
        super().__init__(goal)
        self.update_attributes(goal)

    def to_entity(self) -> Goal:
        goal = object.__new__(Goal)
        self.fill_entity(goal)

        goal.status = enum_utils.instantiate_enum_from_str_name(GoalStatus, self.status)
        goal.description = self.description
        goal.due_date = self.due_date
        goal.type = enum_utils.instantiate_enum_from_str_name(GoalType, self.feedback_type)
        goal.team = self.team_db.to_entity() if self.team_db else None
        goal.user = self.user_db.to_entity() if self.user_db else None
        goal.parent_goal_id = self.parent_goal_id

        return goal

    def update_attributes(self, goal: Goal):
        super().update_attributes(goal)

        self.status = goal.status.name
        self.description = goal.description
        self.feedback_type = goal.type.name
        self.due_date = goal.due_date
        self.user_id = goal.user.id if goal.user else None
        self.team_id = goal.team.id if goal.team else None
        self.parent_goal_id = goal.parent_goal_id
