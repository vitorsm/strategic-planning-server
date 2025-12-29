from sqlalchemy import Column, UUID, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.meeting import Meeting


class MeetingUserDB(Base):
    __tablename__ = "meeting_has_user"
    meeting_id = Column(UUID, ForeignKey("meeting.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)

    user_db = relationship("UserDB", foreign_keys=[user_id], lazy="joined")

    def __init__(self, meeting_id: UUID, user_id: UUID):
        self.meeting_id = meeting_id
        self.user_id = user_id

    def to_entity(self):
        return self.user_db.to_entity()

    def update_attributes(self, entity):
        pass


class MeetingNoteDB(Base):
    __tablename__ = "meeting_note"
    id = Column(UUID, primary_key=True)
    meeting_id = Column(UUID, ForeignKey("meeting.id"), nullable=False)
    note = Column(Text, nullable=False)

    def __init__(self, note_id: UUID, meeting_id: UUID, note: str):
        self.id = note_id
        self.meeting_id = meeting_id
        self.note = note

    def to_entity(self) -> str:
        return self.note

    def update_attributes(self, entity):
        pass


class MeetingDB(GenericEntityDB, Base[Meeting]):
    __tablename__ = "meeting"

    meeting_date = Column(DateTime, nullable=False)

    users = relationship("MeetingUserDB", lazy="joined",
                         foreign_keys="MeetingDB.id", remote_side="MeetingUserDB.meeting_id",
                         primaryjoin="MeetingDB.id == MeetingUserDB.meeting_id",
                         uselist=True, cascade="all, delete-orphan",
                         single_parent=True)

    notes = relationship("MeetingNoteDB", lazy="joined",
                         foreign_keys="MeetingDB.id", remote_side="MeetingNoteDB.meeting_id",
                         primaryjoin="MeetingDB.id == MeetingNoteDB.meeting_id",
                         uselist=True, cascade="all, delete-orphan",
                         single_parent=True)

    def __init__(self, meeting: Meeting):
        super().__init__(meeting)
        self.update_attributes(meeting)

    def update_attributes(self, meeting: Meeting):
        super().update_attributes(meeting)
        self.meeting_date = meeting.meeting_date
        self.users = [MeetingUserDB(meeting.id, user.id) for user in meeting.users] if meeting.users else []
        self.notes = [MeetingNoteDB(self._generate_note_id(meeting.id, i), meeting.id, note) 
                      for i, note in enumerate(meeting.notes)] if meeting.notes else []

    def _generate_note_id(self, meeting_id: UUID, index: int) -> UUID:
        from uuid import uuid5, NAMESPACE_OID
        return uuid5(NAMESPACE_OID, f"{meeting_id}-note-{index}")

    def to_entity(self) -> Meeting:
        meeting = object.__new__(Meeting)
        self.fill_entity(meeting)
        return meeting

    def fill_entity(self, meeting: Meeting):
        super().fill_entity(meeting)
        meeting.meeting_date = self.meeting_date
        meeting.users = [user_db.to_entity() for user_db in self.users]
        meeting.notes = [note_db.to_entity() for note_db in self.notes]

