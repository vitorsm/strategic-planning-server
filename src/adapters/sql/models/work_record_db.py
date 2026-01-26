from sqlalchemy import Column, UUID, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.work_record import WorkRecord


class WorkRecordUserDB(Base):
    __tablename__ = "work_record_has_user"
    work_record_id = Column(UUID, ForeignKey("work_record.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)

    user_db = relationship("UserDB")
    work_record_db = relationship("WorkRecordDB", foreign_keys=[work_record_id])

    def __init__(self, work_record_id: UUID, user_id: UUID):
        self.work_record_id = work_record_id
        self.user_id = user_id

    def to_entity(self):
        return self.user_db.to_entity()

    def update_attributes(self, entity):
        pass


class WorkRecordDB(GenericEntityDB, Base[WorkRecord]):
    __tablename__ = "work_record"

    description = Column(Text, nullable=True)
    task_type_id = Column(UUID, ForeignKey("task_type.id"), nullable=False)
    goal_id = Column(UUID, ForeignKey("goal.id"), nullable=True)
    team_id = Column(UUID, ForeignKey("team.id"), nullable=True)

    task_type_db = relationship("TaskTypeDB", foreign_keys=[task_type_id], lazy="joined")
    goal_db = relationship("GoalDB", foreign_keys=[goal_id], lazy="joined")
    team_db = relationship("TeamDB", foreign_keys=[team_id], lazy="joined")

    users = relationship(
        "WorkRecordUserDB",
        back_populates="work_record_db",
        cascade="all, delete-orphan"
    )

    def __init__(self, work_record: WorkRecord):
        super().__init__(work_record)
        self.update_attributes(work_record)

    def update_attributes(self, work_record: WorkRecord):
        super().update_attributes(work_record)
        self.description = work_record.description
        self.task_type_id = work_record.task_type.id
        self.goal_id = work_record.goal.id if work_record.goal else None
        self.team_id = work_record.team.id if work_record.team else None
        self.users = [WorkRecordUserDB(work_record.id, user.id) for user in work_record.users] if work_record.users else []

    def to_entity(self) -> WorkRecord:
        work_record = object.__new__(WorkRecord)
        self.fill_entity(work_record)
        return work_record

    def fill_entity(self, work_record: WorkRecord):
        super().fill_entity(work_record)
        work_record.description = self.description
        work_record.task_type = self.task_type_db.to_entity()
        work_record.goal = self.goal_db.to_entity() if self.goal_db else None
        work_record.team = self.team_db.to_entity() if self.team_db else None
        work_record.users = [user_db.to_entity() for user_db in self.users]

