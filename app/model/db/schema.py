from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

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


class Group(Base):
    __tablename__ = 'Group'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    status_id = Column(ForeignKey("Status.id"))

    status = relationship("Status")


class UserGroup(Base):
    __tablename__ = 'UserGroup'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("Status.id"), nullable=False)
    group_id = Column(ForeignKey("Group.id"), nullable=False)

    group = relationship("Group", backref="user_groups")
    user = relationship("User", backref="user_groups")
