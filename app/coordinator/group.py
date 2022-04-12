from app.group.group_db_executor import GroupDbExecutor
from app.model.db.schema import Group
from app.group.fastapi.group_out.basic_group_out import BasicGroupOut


BasicGroupOut = BasicGroupOut


def get_group_by_id(group_id: int) -> Group:
    return GroupDbExecutor.get_group_by_id(group_id)
