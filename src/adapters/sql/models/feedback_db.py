from sqlalchemy import Column, Text, String, UUID, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base, Entity
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.feedback import Feedback, FeedbackType
from src.utils import enum_utils


class FeedbackDB(GenericEntityDB, Base[Feedback]):
    __tablename__ = "feedback"

    description = Column(Text, nullable=True)
    feedback_type = Column(String(255), nullable=False)
    user_from = Column(UUID, ForeignKey("user.id"), nullable=False)
    user_to = Column(UUID, ForeignKey("user.id"), nullable=False)
    delivered = Column(Boolean, nullable=False, default=False)

    user_from_db = relationship("UserDB", foreign_keys="FeedbackDB.user_from", lazy="joined")
    user_to_db = relationship("UserDB", foreign_keys="FeedbackDB.user_to", lazy="joined")

    def __init__(self, feedback: Feedback):
        super().__init__(feedback)
        self.update_attributes(feedback)

    def to_entity(self) -> Entity:
        feedback = object.__new__(Feedback)
        self.fill_entity(feedback)

        feedback.delivered = self.delivered
        feedback.type = enum_utils.instantiate_enum_from_str_name(FeedbackType, self.feedback_type)
        feedback.user_from = self.user_from_db.to_entity()
        feedback.user_to = self.user_to_db.to_entity()
        feedback.description = self.description

        return feedback

    def update_attributes(self, feedback: Feedback):
        super().update_attributes(feedback)

        self.feedback_type = feedback.type.name
        self.user_from = feedback.user_from.id
        self.user_to = feedback.user_to.id
        self.delivered = feedback.delivered
        self.description = feedback.description
