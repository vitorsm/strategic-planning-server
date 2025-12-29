from uuid import UUID

from sqlalchemy import Column, UUID as SQLUUID, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.strategic_plan import StrategicPlan, TaskTypePlan


class StrategicPlanTaskTypePlanDB(Base):
    __tablename__ = "strategic_plan_has_task_type"
    strategic_plan_id = Column(SQLUUID, ForeignKey("strategic_plan.id"), primary_key=True)
    task_type_id = Column(SQLUUID, ForeignKey("task_type.id"), primary_key=True)
    percentage = Column(Float, nullable=False)

    task_type_db = relationship("TaskTypeDB", foreign_keys=[task_type_id], lazy="joined")

    def __init__(self, strategic_plan_id: UUID, task_type_id: UUID, percentage: float):
        self.strategic_plan_id = strategic_plan_id
        self.task_type_id = task_type_id
        self.percentage = percentage

    def to_entity(self) -> TaskTypePlan:
        return TaskTypePlan(task_type=self.task_type_db.to_entity(), percentage=self.percentage)

    def update_attributes(self, entity):
        pass


class StrategicPlanGoalDB(Base):
    __tablename__ = "strategic_plan_has_goal"
    strategic_plan_id = Column(SQLUUID, ForeignKey("strategic_plan.id"), primary_key=True)
    goal_id = Column(SQLUUID, ForeignKey("goal.id"), primary_key=True)

    goal_db = relationship("GoalDB", foreign_keys=[goal_id], lazy="joined")

    def __init__(self, strategic_plan_id: UUID, goal_id: UUID):
        self.strategic_plan_id = strategic_plan_id
        self.goal_id = goal_id

    def to_entity(self):
        return self.goal_db.to_entity()

    def update_attributes(self, entity):
        pass


class StrategicPlanDB(GenericEntityDB, Base[StrategicPlan]):
    __tablename__ = "strategic_plan"

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    task_type_plans = relationship("StrategicPlanTaskTypePlanDB", lazy="joined",
                                   foreign_keys="StrategicPlanDB.id",
                                   remote_side="StrategicPlanTaskTypePlanDB.strategic_plan_id",
                                   primaryjoin="StrategicPlanDB.id == StrategicPlanTaskTypePlanDB.strategic_plan_id",
                                   uselist=True, cascade="all, delete-orphan",
                                   single_parent=True)

    goals = relationship("StrategicPlanGoalDB", lazy="joined",
                         foreign_keys="StrategicPlanDB.id",
                         remote_side="StrategicPlanGoalDB.strategic_plan_id",
                         primaryjoin="StrategicPlanDB.id == StrategicPlanGoalDB.strategic_plan_id",
                         uselist=True, cascade="all, delete-orphan",
                         single_parent=True)

    def __init__(self, strategic_plan: StrategicPlan):
        super().__init__(strategic_plan)
        self.update_attributes(strategic_plan)

    def update_attributes(self, strategic_plan: StrategicPlan):
        super().update_attributes(strategic_plan)
        self.start_date = strategic_plan.start_date
        self.end_date = strategic_plan.end_date
        self.task_type_plans = [
            StrategicPlanTaskTypePlanDB(strategic_plan.id, ttp.task_type.id, ttp.percentage)
            for ttp in strategic_plan.task_type_plans
        ] if strategic_plan.task_type_plans else []
        self.goals = [
            StrategicPlanGoalDB(strategic_plan.id, goal.id)
            for goal in strategic_plan.goals
        ] if strategic_plan.goals else []

    def to_entity(self) -> StrategicPlan:
        strategic_plan = object.__new__(StrategicPlan)
        self.fill_entity(strategic_plan)
        return strategic_plan

    def fill_entity(self, strategic_plan: StrategicPlan):
        super().fill_entity(strategic_plan)
        strategic_plan.start_date = self.start_date
        strategic_plan.end_date = self.end_date
        strategic_plan.task_type_plans = [ttp_db.to_entity() for ttp_db in self.task_type_plans]
        strategic_plan.goals = [goal_db.to_entity() for goal_db in self.goals]

