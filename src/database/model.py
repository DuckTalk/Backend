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
    privatemessages = relationship("PrivateMessage", cascade="all,delete", uselist=True, backref="user")

class Group(Base):
    """Group representation."""

    __tablename__ = "group"
    group_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    groupname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    groupusers = relationship("GroupUser", cascade="all,delete", uselist=True, backref="group")
    groupmessages = relationship("GroupMessage", cascade="all,delete", uselist=True, backref="group")

class GroupUser(Base):
    """Crosstable between User and Group."""

    __tablename__ = "groupuser"
    groupuser_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    isadmin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("user.user_id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("group.group_id"))

class PrivateMessage(Base):
    """PrivateMessage representation."""

    __tablename__ = "privatemessage"
    message_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    receiver_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("user.user_id"))

class GroupMessage(Base):
    """GroupMessage representation."""

    __tablename__ = "groupmessage"
    message_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    receiver_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("group.group_id"))
