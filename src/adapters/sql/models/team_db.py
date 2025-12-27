from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.team import Team


class TeamUserDB(Base):
    __tablename__ = "team_has_user"
    team_id = Column(UUID, ForeignKey("team.id"), primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), primary_key=True)

    def __init__(self, team_id: UUID, user_id: UUID):
        self.team_id = team_id
        self.user_id = user_id

    def to_entity(self):
        pass

    def update_attributes(self, entity):
        pass


class TeamDB(GenericEntityDB, Base[Team]):
    __tablename__ = "team"

    users = relationship("TeamUserDB", lazy="select",
                         foreign_keys="TeamDB.id", remote_side="TeamUserDB.team_id",
                         primaryjoin="TeamDB.id == TeamUserDB.team_id",
                         uselist=True, cascade="all, delete-orphan",
                         single_parent=True)

    def __init__(self, team: Team):
        super().__init__(team)
        self.update_attributes(team)

    def update_attributes(self, team: Team):
        super().update_attributes(team)
        self.users = [TeamUserDB(team.id, user_id) for user_id in team.members_ids] if team.members_ids else []

    def to_entity(self) -> Team:
        team = object.__new__(Team)
        self.fill_entity(team)
        return team

    def fill_entity(self, team: Team):
        super().fill_entity(team)
        team.members_ids = [user.user_id for user in self.users]
