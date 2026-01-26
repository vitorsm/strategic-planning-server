from sqlalchemy import Column, UUID, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.team import Team


class TeamUserDB(Base):
    __tablename__ = "team_has_user"
    team_id = Column(UUID, ForeignKey("team.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)

    team_db = relationship("TeamDB", back_populates="users")
    user_db = relationship("UserDB")

    def __init__(self, team_id: UUID, user_id: UUID):
        self.team_id = team_id
        self.user_id = user_id

    def to_entity(self):
        return self.user_db.to_entity()

    def update_attributes(self, entity):
        pass


class TeamDB(GenericEntityDB, Base[Team]):
    __tablename__ = "team"

    description = Column(Text, nullable=True)

    users = relationship(
        "TeamUserDB",
        back_populates="team_db",
        cascade="all, delete-orphan"
    )

    def __init__(self, team: Team):
        super().__init__(team)
        self.update_attributes(team)

    def update_attributes(self, team: Team):
        super().update_attributes(team)
        self.description = team.description
        self.users = [TeamUserDB(team.id, user.id) for user in team.members] if team.members else []

    def to_entity(self) -> Team:
        team = object.__new__(Team)
        self.fill_entity(team)
        return team

    def fill_entity(self, team: Team):
        super().fill_entity(team)
        team.description = self.description
        team.members = [user.to_entity() for user in self.users]
