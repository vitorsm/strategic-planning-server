from sqlalchemy import Column, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base, Entity
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.reminder import Reminder


class ReminderDB(GenericEntityDB, Base[Reminder]):
    __tablename__ = "reminder"

    description = Column(Text, nullable=True)
    to_user_id = Column(UUID, ForeignKey("user.id"), nullable=False)

    to_user_db = relationship("UserDB", foreign_keys="ReminderDB.to_user_id", lazy="joined")

    def __init__(self, reminder: Reminder):
        super().__init__(reminder)
        self.update_attributes(reminder)

    def to_entity(self) -> Entity:
        reminder = object.__new__(Reminder)
        self.fill_entity(reminder)

        reminder.to_user = self.to_user_db.to_entity()
        reminder.description = self.description

        return reminder

    def update_attributes(self, reminder: Reminder):
        super().update_attributes(reminder)

        self.to_user_id = reminder.to_user.id
        self.description = reminder.description

