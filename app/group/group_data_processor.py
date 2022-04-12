from typing import Optional, List
from http import HTTPStatus

from fastapi.responses import Response

from app.group.fastapi.group_in.group_edit_in import GroupEditIn
from app.group.fastapi.group_in.group_new_in import GroupNewIn
from app.group.fastapi.group_out.detailed_group_out import DetailedGroupOut
from app.group.group_db_executor import GroupDbExecutor
from app.model.db.schema import Group
from app.model.error.error import Error
from app.model.db.constant.status import Status as StatusConstant


class GroupDataProcessor:
    @classmethod
    def create_group(cls, group_new_in: GroupNewIn, response: Response) -> Response:
        existing_group: Group = GroupDbExecutor.get_group_by_name(group_new_in.name)

        if existing_group:
            raise Error.group_already_exists

        group_id: int = GroupDbExecutor.create_group(group_new_in)

        response.headers["location"] = f"/groups/{group_id}"
        response.status_code = HTTPStatus.CREATED

        return response

    @classmethod
    def edit_group(cls, group_id: int, group_in: GroupEditIn) -> Response:
        group: Optional[Group] = GroupDbExecutor.get_group_by_id(group_id)

        if not group:
            raise Error.group_not_exists

        GroupDbExecutor.edit_group(group, group_in)

        return Response(status_code=HTTPStatus.NO_CONTENT)

    @classmethod
    def change_group_status(cls, group_id: int, status_id: int) -> Response:
        is_status_exist: bool = StatusConstant.has_value(status_id)

        if not is_status_exist:
            raise Error.status_not_exists

        group: Optional[Group] = GroupDbExecutor.get_group_by_id(group_id)

        if not group:
            raise Error.group_not_exists

        GroupDbExecutor.change_group_status(group, status_id)

        return Response(status_code=HTTPStatus.NO_CONTENT)

    @classmethod
    def get_all_groups(cls) -> List[DetailedGroupOut]:
        return [
            DetailedGroupOut.from_db(group) for group in GroupDbExecutor.get_groups()
        ]
