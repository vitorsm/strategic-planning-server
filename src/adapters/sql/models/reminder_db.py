from sqlalchemy import Column, String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base, Entity
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.reminder import Reminder, ReminderStatus
from src.utils import enum_utils


class ReminderDB(GenericEntityDB, Base[Reminder]):
    __tablename__ = "reminder"

    description = Column(Text, nullable=True)
    status = Column(String(100), nullable=False)
    to_user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    related_user_id = Column(UUID, ForeignKey("user.id"), nullable=True)
    related_team_id = Column(UUID, ForeignKey("team.id"), nullable=True)

    to_user_db = relationship("UserDB", foreign_keys="ReminderDB.to_user_id", lazy="joined")
    related_user_db = relationship("UserDB", foreign_keys="ReminderDB.related_user_id", lazy="joined")
    related_team_db = relationship("TeamDB", foreign_keys="ReminderDB.related_team_id", lazy="joined")

    def __init__(self, reminder: Reminder):
        super().__init__(reminder)
        self.update_attributes(reminder)

    def to_entity(self) -> Entity:
        reminder = object.__new__(Reminder)
        self.fill_entity(reminder)

        reminder.to_user = self.to_user_db.to_entity()
        reminder.status = enum_utils.instantiate_enum_from_str_name(ReminderStatus, self.status)
        reminder.related_user = self.related_user_db.to_entity() if self.related_user_db else None
        reminder.related_team = self.related_team_db.to_entity() if self.related_team_db else None
        reminder.description = self.description

        return reminder

    def update_attributes(self, reminder: Reminder):
        super().update_attributes(reminder)

        self.to_user_id = reminder.to_user.id
        self.status = reminder.status.name
        self.related_user_id = reminder.related_user.id if reminder.related_user else None
        self.related_team_id = reminder.related_team.id if reminder.related_team else None
        self.description = reminder.description

