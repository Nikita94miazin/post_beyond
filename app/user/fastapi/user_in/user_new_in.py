import re

from app.model.camel_model import CamelModel
from pydantic import validator

from app.model.error.error import Error
from app.model.db.constant.role import Role as RoleConstant


class UserNewIn(CamelModel):
    first_name: str
    last_name: str
    email: str
    role_id: int
    group_id: int

    @validator('email')
    def validate_user_email(cls, email: str) -> str:
        if not bool(re.match(r"^\S+@.+\..{2,}$", email)):
            raise Error.invalid_email_format

        return email

    @validator('role_id')
    def validate_user_role(cls, role_id: int) -> int:
        if not RoleConstant.has_value(role_id):
            raise Error.role_not_exist

        return role_id
