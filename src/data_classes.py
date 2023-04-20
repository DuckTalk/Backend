from __future__ import annotations
from dataclasses import dataclass

from database.model import User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb

@dataclass
class User():
    user_id: int
    username: str
    email: str
    publickey: str

    def to_json_obj(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "publickey": self.publickey
        }

@dataclass
class Group():
    group_id: int
    groupname: str
    description: str
    members: list[tuple[User, bool]]

    def to_json_obj(self) -> dict:
        members = {}
        c = 0
        while (c < len(self.members)):
            members[c] = {
                "user_id": self.members[c][0].user_id,
                "admin": self.members[c][1]
            }
            c += 1
        return {
            "group_id": self.group_id,
            "groupname": self.groupname,
            "description": self.description,
            "members": members
        }

@dataclass
class Message():
    message_id: int
    sender: User
    receiver: User|Group
    content: str
