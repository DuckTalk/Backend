"""Declaring data models"""

import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.hybrid import hybrid_property

Base = sqlalchemy.ext.declarative.declarative_base()

# pylint: disable=R0903

class User(Base):
    """User representation."""

    __tablename__ = "user"
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=False)
    publickey = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    salt = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_pw = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    token = sqlalchemy.Column(sqlalchemy.String, unique=False)
    groupusers = relationship("GroupUser", cascade="all,delete", uselist=True, backref="user")

class GroupUser(Base):
    """Crosstable between User and Group."""

    __tablename__ = "groupuser"
    groupuser_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    isadmin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("user.user_id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("group.group_id"))
    messages = relationship("Message", cascade="all,delete", uselist=True, backref="groupuser")

class Group(Base):
    """Group representation."""

    __tablename__ = "group"
    group_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    is_privatechat = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    groupname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    groupusers = relationship("GroupUser", cascade="all,delete", uselist=True, backref="group")
    groupmessages = relationship("Message", cascade="all,delete", uselist=True, backref="group")

class Message(Base):
    """Message representation."""

    __tablename__ = "message"
    message_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("group.group_id"))
    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("groupuser.groupuser_id"))
