from http import HTTPStatus
from typing import List

from fastapi.responses import Response

from app.coordinator import get_group_by_id
from app.model.db.schema import User, Group, UserGroup
from app.model.error.error import Error
from app.user.fastapi.user_in.user_new_in import UserNewIn
from app.user.fastapi.user_out.user_out import UserOut
from app.user.user_db_executor import UserDbExecutor
from app.model.db.constant.status import Status as StatusConstant


class UserDataProcessor:
    @classmethod
    def get_all_users(cls) -> List[UserOut]:
        return [
            UserOut.from_db(user) for user in UserDbExecutor.get_users()
        ]

    @classmethod
    def create_user(cls, user_new_in: UserNewIn, response: Response) -> Response:
        user: User = UserDbExecutor.get_user_by_email(user_new_in.email)

        if user:
            raise Error.user_with_same_email_exist

        group: Group = get_group_by_id(user_new_in.group_id)

        if not group:
            raise Error.group_not_exist

        user_id: int = UserDbExecutor.create_user(user_new_in)

        response.headers["location"] = f"/users/{user_id}"
        response.status_code = HTTPStatus.CREATED

        return response

    @classmethod
    def delete_user(cls, user_id: int) -> Response:
        user: User = UserDbExecutor.get_user_by_id(user_id)

        if not user:
            raise Error.user_not_exist

        UserDbExecutor.delete_user(user)

        return Response(status_code=HTTPStatus.NO_CONTENT)

    @classmethod
    def change_user_status(cls, user_id: int, status_id: int) -> Response:
        is_status_exist: bool = StatusConstant.has_value(status_id)

        if not is_status_exist:
            raise Error.status_not_exist

        user: User = UserDbExecutor.get_user_by_id(user_id)

        if not user:
            raise Error.user_not_exist

        UserDbExecutor.change_user_status(user, status_id)

        return Response(status_code=HTTPStatus.NO_CONTENT)

    @classmethod
    def add_user_to_group(cls, user_id: int, group_id: int) -> Response:
        user: User = UserDbExecutor.get_user_by_id(user_id)

        if not user:
            raise Error.user_not_exist

        group: Group = get_group_by_id(group_id)

        if not group:
            raise Error.group_not_exist

        user_group: UserGroup = UserDbExecutor.get_user_group(user_id, group_id)

        if user_group:
            raise Error.user_is_member

        UserDbExecutor.add_user_to_group(user_id, group_id)

        return Response(status_code=HTTPStatus.NO_CONTENT)

    @classmethod
    def delete_user_from_group(cls, user_id: int, group_id: int) -> Response:
        user: User = UserDbExecutor.get_user_by_id(user_id)

        if not user:
            raise Error.user_not_exist

        group: Group = get_group_by_id(group_id)

        if not group:
            raise Error.group_not_exist

        user_group: UserGroup = UserDbExecutor.get_user_group(user_id, group_id)

        if not user_group:
            raise Error.user_is_not_member

        UserDbExecutor.delete_user_from_group(user_group)

        return Response(status_code=HTTPStatus.NO_CONTENT)
