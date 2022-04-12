from typing import List
from datetime import datetime

from app.model.camel_model import CamelModel
from app.model.db.schema import User
from app.model.db.constant.status import Status as StatusConstant
from app.coordinator.group import BasicGroupOut


class UserOut(CamelModel):
    full_name: str
    role: str
    status: str
    creation_time: datetime
    active_group_number: int
    groups: List[BasicGroupOut]

    @classmethod
    def from_db(cls, user: User):
        return cls(
            full_name=f"{user.first_name} {user.last_name}",
            role=user.role.name,
            status=user.status.name,
            creation_time=user.creation_date,
            active_group_number=len(
                [
                    user_group for user_group in user.user_groups
                    if user_group.group.status_id == StatusConstant.active.value
                ]
            ),
            groups=[
                BasicGroupOut.from_db(user_group.group) for user_group in user.user_groups
            ]
        )
