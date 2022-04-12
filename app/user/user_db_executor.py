from typing import Optional, List

from fastapi_sqlalchemy import db
from sqlalchemy import func

from app.model.db.db_executor import DbExecutor
from app.model.db.schema import User, UserGroup
from app.model.error.error import Error
from app.user.fastapi.user_in.user_new_in import UserNewIn


class UserDbExecutor(DbExecutor):
    @classmethod
    def get_user_by_email(cls, email: str) -> Optional[User]:
        return db.session.query(User).filter(func.lower(User.email) == func.lower(email)).first()

    @classmethod
    def get_user_by_id(cls, user_id: int) -> Optional[User]:
        return db.session.query(User).filter(User.id == user_id).first()

    @classmethod
    def create_user(cls, user_new_in: UserNewIn) -> int:
        user: User = User(user_new_in.first_name, user_new_in.last_name, user_new_in.email, user_new_in.role_id)

        db.session.add(user)
        cls._flush()

        cls.add_user_to_group(user.id, user_new_in.group_id, False)

        cls._commit()

        return user.id

    @classmethod
    def add_user_to_group(cls, user_id: int, group_id: int, commit: bool = True) -> None:
        user_group: UserGroup = UserGroup(user_id, group_id)

        db.session.add(user_group)

        if commit:
            cls._commit()
        else:
            cls._flush()

    @classmethod
    def delete_user(cls, user: User) -> None:
        db.session.delete(user)
        cls._commit()

    @classmethod
    def change_user_status(cls, user: User, status_id: int) -> None:
        if user.status_id == status_id:
            raise Error.status_is_the_same

        user.status_id = status_id

        cls._commit()

    @classmethod
    def delete_user_from_group(cls, user_group: UserGroup) -> None:
        db.session.delete(user_group)

        cls._commit()

    @classmethod
    def get_user_group(cls, user_id: int, group_id: int) -> Optional[UserGroup]:
        return db.session.query(UserGroup).filter(UserGroup.user_id == user_id, UserGroup.group_id == group_id).first()

    @classmethod
    def get_users(cls) -> List[User]:
        return db.session.query(User).order_by(User.first_name, User.last_name).all()
