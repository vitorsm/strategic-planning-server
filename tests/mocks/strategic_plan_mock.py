from datetime import datetime, timedelta
import random
from typing import List

from src.entities.goal import Goal
from src.entities.strategic_plan import StrategicPlan, TaskTypePlan
from tests.mocks import task_type_mock, goal_mock, generic_entity_mock, DEFAULT_CREATED_AT

now = datetime.now()


def get_valid_strategic_plan(task_type_plans: List[TaskTypePlan] = None, goals: List[Goal] = None,
                             start_date: datetime = now, end_date: datetime = now, **kwargs) -> StrategicPlan:
                             
    if not kwargs.get("name"):
        kwargs["name"] = f"Task type {int(random.random() * 1000)}"
        
    strategic_plan = object.__new__(StrategicPlan)
    generic_entity_mock.fill_valid_entity(strategic_plan, **kwargs)
    strategic_plan.task_type_plans = task_type_plans or [TaskTypePlan(task_type=task_type_mock.get_valid_task_type(),
                                                                      percentage=10)]
    strategic_plan.goals = goals or [goal_mock.get_valid_goal()]
    strategic_plan.start_date = start_date
    strategic_plan.end_date = end_date
    return strategic_plan


def get_default_strategic_plan() -> StrategicPlan:
    strategic_plan = object.__new__(StrategicPlan)
    generic_entity_mock.fill_default_entity(strategic_plan, "Strategic Plan 1")
    strategic_plan.task_type_plans = [TaskTypePlan(task_type=task_type_mock.get_default_task_type(),
                                                   percentage=10)]
    strategic_plan.goals = [goal_mock.get_default_goal()]
    strategic_plan.start_date = DEFAULT_CREATED_AT + timedelta(days=10)
    strategic_plan.end_date = DEFAULT_CREATED_AT + timedelta(days=20)

    return strategic_plan
