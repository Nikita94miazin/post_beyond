from app.model.camel_model import CamelModel
from app.model.db.schema import Group


class BasicGroupOut(CamelModel):
    name: str
    status: str

    @classmethod
    def from_db(cls, group: Group):
        return cls(
            name=group.name,
            status=group.status.name
        )
