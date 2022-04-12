from typing import Optional, List

from fastapi_sqlalchemy import db
from sqlalchemy import func

from app.group.fastapi.group_in.group_edit_in import GroupEditIn
from app.group.fastapi.group_in.group_new_in import GroupNewIn
from app.model.db.db_executor import DbExecutor
from app.model.db.schema import Group
from app.model.error.error import Error


class GroupDbExecutor(DbExecutor):
    @classmethod
    def create_group(cls, group_new_in: GroupNewIn) -> int:
        group: Group = Group(group_new_in.name)
        db.session.add(group)
        cls._commit()
        return group.id

    @classmethod
    def get_group_by_name(cls, name: str) -> Optional[Group]:
        return db.session.query(Group).filter(func.lower(Group.name) == func.lower(name)).first()

    @classmethod
    def get_group_by_id(cls, group_id: int) -> Optional[Group]:
        return db.session.query(Group).filter(Group.id == group_id).first()

    @classmethod
    def edit_group(cls, group: Group, group_in: GroupEditIn) -> None:
        # possible to extend by another group params, for example by description
        if not group_in.name:
            raise Error.nothing_changed

        if group_in.name:
            cls.__edit_group_name(group, group_in.name)

        cls._commit()

    @classmethod
    def __edit_group_name(cls, group: Group, new_name: str) -> None:
        if group.name == new_name:
            raise Error.group_name_is_the_same

        if cls.get_group_by_name(new_name):
            raise Error.group_already_exist

        group.name = new_name

    @classmethod
    def change_group_status(cls, group: Group, status_id: int) -> None:
        if group.status_id == status_id:
            raise Error.status_is_the_same

        group.status_id = status_id

        cls._commit()

    @classmethod
    def get_groups(cls) -> List[Group]:
        return db.session.query(Group).order_by(Group.name).all()
