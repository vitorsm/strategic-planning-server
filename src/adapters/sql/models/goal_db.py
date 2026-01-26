import copy

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
    parent_goal_db = relationship("GoalDB", foreign_keys=[parent_goal_id], lazy="joined",
                                  remote_side="GoalDB.id", back_populates="children")

    children = relationship(
        "GoalDB",
        back_populates="parent_goal_db",
        cascade="all, delete-orphan"
    )

    def __init__(self, goal: Goal):
        super().__init__(goal)
        self.update_attributes(goal)

    def to_entity(self, parent_goal: Goal = None) -> Goal:
        goal = object.__new__(Goal)
        self.fill_entity(goal)

        goal.status = enum_utils.instantiate_enum_from_str_name(GoalStatus, self.status)
        goal.description = self.description
        goal.due_date = self.due_date
        goal.type = enum_utils.instantiate_enum_from_str_name(GoalType, self.feedback_type)
        goal.team = self.team_db.to_entity() if self.team_db else None
        goal.user = self.user_db.to_entity() if self.user_db else None

        if parent_goal:
            goal.parent_goal = parent_goal
        else:
            goal.parent_goal = self.parent_goal_db.to_entity() if self.parent_goal_db else None

        parent_goal = copy.copy(goal)
        parent_goal.children = []
        goal.children = [child.to_entity(parent_goal=parent_goal) for child in self.children] if self.children else []

        return goal

    def update_attributes(self, goal: Goal):
        super().update_attributes(goal)

        self.status = goal.status.name
        self.description = goal.description
        self.feedback_type = goal.type.name
        self.due_date = goal.due_date
        self.user_id = goal.user.id if goal.user else None
        self.team_id = goal.team.id if goal.team else None
        self.parent_goal_id = goal.parent_goal.id if goal.parent_goal else None
