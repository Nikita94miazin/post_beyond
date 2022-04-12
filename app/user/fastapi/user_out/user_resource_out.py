from app.model.camel_model import CamelModel
from app.model.db.schema import User


class UserResourceOut(CamelModel):
    full_name: str
    resource_uri: str

    @classmethod
    def from_db(cls, user: User):
        return cls(
            full_name=f"{user.first_name} {user.last_name}",
            resource_uri=f"/users/{user.id}"
        )
