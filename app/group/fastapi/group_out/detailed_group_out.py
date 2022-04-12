from typing import List

from app.model.db.schema import Group
from app.group.fastapi.group_out.basic_group_out import BasicGroupOut
from app.coordinator import UserResourceOut


class DetailedGroupOut(BasicGroupOut):
    users: List[UserResourceOut]

    @classmethod
    def from_db(cls, group: Group):
        return cls(
            name=group.name,
            status=group.status.name,
            users=[
                UserResourceOut.from_db(user_group.user) for user_group in group.user_groups
            ]
        )
