from typing import Optional

from app.model.camel_model import CamelModel


class GroupEditIn(CamelModel):
    name: Optional[str]
