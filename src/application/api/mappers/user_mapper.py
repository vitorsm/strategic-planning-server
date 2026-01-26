from typing import Optional

from src.application.api.mappers.generic_mapper import GenericMapper, register_new_mapper
from src.entities.user import User


class UserMapper(GenericMapper[User]):

    @classmethod
    def to_dto(cls, user: Optional[User]) -> Optional[dict]:
        dto = super().to_dto(user)
        if dto:
            user_name = dto["name"]
            user_name_parts = user_name.split(" ")

            dto["password"] = None
            dto["initials"] = user_name_parts[0][0]
            if len(user_name_parts) > 1:
                dto["initials"] += user_name_parts[1][0]

        return dto


register_new_mapper(UserMapper)
