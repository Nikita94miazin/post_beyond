from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from app.model.db.constant.status import Status as StatusConstant


Base = declarative_base()


class Role(Base):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Status(Base):
    __tablename__ = 'Status'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False)
    status_id = Column(ForeignKey("Status.id"), nullable=False)
    role_id = Column(ForeignKey("Role.id"), nullable=False)

    status = relationship("Status")
    role = relationship("Role")

    def __init__(self, first_name: str, last_name: str, email: str, role_id: int) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.role_id: int = role_id

        self.status_id: str = StatusConstant.active.value
        self.creation_date: datetime = datetime.now()


class Group(Base):
    __tablename__ = 'Group'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False)
    status_id = Column(ForeignKey("Status.id"))

    status = relationship("Status")

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.creation_date: datetime = datetime.now()
        self.status_id: int = StatusConstant.active.value

    def change_status(self, status: StatusConstant) -> None:
        self.status_id = status.value


class UserGroup(Base):
    __tablename__ = 'UserGroup'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("User.id"), nullable=False)
    group_id = Column(ForeignKey("Group.id"), nullable=False)

    group = relationship("Group", backref=backref("user_groups"), order_by="Group.name.asc()")
    user = relationship(
        "User",
        backref=backref(
            "user_groups",
            cascade="all, delete-orphan"
        ),
        order_by='User.first_name.asc(), User.last_name.asc()'
    )

    def __init__(self, user_id: int, group_id: int) -> None:
        self.user_id: int = user_id
        self.group_id: int = group_id
