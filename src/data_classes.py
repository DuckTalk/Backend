from __future__ import annotations
from dataclasses import dataclass

from database.model import User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           PrivateMessage as PrivateMessagedb, GroupMessage as GroupMessagedb

@dataclass
class User():
    user_id: int
    username: str
    email: str
    publickey: str

    @staticmethod
    def from_userdb(user_db: Userdb) -> User:
        return User(user_db.user_id, user_db.username, user_db.email, user_db.publickey)

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
    members: dict[int, dict[str, User|bool]]

@dataclass
class Message():
    message_id: int
    sender_id: int
    receiver: dict[str, User|Group|int]
    content: str
