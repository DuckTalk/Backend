"""Module for managing the database"""

# pylint: disable=E0401, R0402

from threading import Lock
from typing import List

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           Message as Messagedb
from data_classes import User, Group, Message
from custom_logger import CustomLogger
logger = CustomLogger().setup()

# pylint: disable=R0801

class DBManager():
    """Class that manages the database"""

    def __init__(self):
        if DBManager.get_inst() is not None:
            return DBManager.get_inst()
            raise Exception("Can only have one DBManager inst at a time")

        db_connection = sqlalchemy.create_engine(f"sqlite:///{self._dbfile}",
                                                 connect_args={'check_same_thread': False})
        Base.metadata.create_all(db_connection)

        session_factory = sessionmaker(db_connection, autoflush=False)
        _session = scoped_session(session_factory)
        self.session = _session()

        DBManager._inst = self

    _inst = None
    lock = Lock()
    _dbfile = "src/database/database.db"

    @staticmethod
    def get_inst():
        return DBManager._inst

    def add_group(self, members: list[Userdb], is_privatechat: bool, groupname: str, description: str) -> int:
        with self.lock:
            stored_group = Groupdb(is_privatechat=is_privatechat, groupname=groupname, description=description)
            self.session.add(stored_group)
            for member in members:
                groupuser = GroupUserdb(isadmin=True)
                self.session.add(groupuser)
                member.groupusers.append(groupuser)
                stored_group.groupusers.append(groupuser)
        self.commit()
        return stored_group.group_id

    def add_message(self, content, sender_id, group_id) -> int:
        with self.lock:
            stored_sender_user = self.get_userdb_from_id(sender_id)
            stored_receiver = self.get_groupdb_from_id(group_id)
            for groupuser in stored_receiver.groupusers:
                if groupuser.user_id == stored_sender_user.user_id:
                    stored_sender: GroupUserdb = groupuser
            message_obj = Messagedb(content=content)
            stored_sender.messages.append(message_obj)
            stored_receiver.groupmessages.append(message_obj)
            self.session.add(message_obj)
        self.commit()
        return message_obj.message_id

    def add_user(self, username, email, publickey, salt, hashed_pw) -> int:
        with self.lock:
            user_obj = Userdb(username=username, email=email, publickey=publickey, salt=salt, hashed_pw=hashed_pw, token=f"user{self.session.query(Userdb).count()}")
            self.session.add(user_obj)
        self.commit()
        return user_obj.user_id

    def commit(self) -> None:
        """Commits changes to database"""

        with self.lock:
            try:
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                logger.error("Committing database changes failed, rolling back")
                self.session.rollback()

    def get_groupdb_from_id(self, group_id: int) -> Groupdb | None:
        return self.session.query(Groupdb).filter(Groupdb.group_id==group_id).first()

    def get_groupuserdb_from_id(self, groupuser_id: int) -> GroupUserdb | None:
        return self.session.query(GroupUserdb).filter(GroupUserdb.groupuser_id==groupuser_id).first()

    def get_messagedb_from_id(self, message_id: int) -> Messagedb | None:
        return self.session.query(Messagedb).filter(Messagedb.message_id==message_id).first()

    def get_userdb_from_email(self, email: str) -> Userdb | None:
        return self.session.query(Userdb).filter(Userdb.email==email).first()

    def get_userdb_from_id(self, user_id: int) -> Userdb | None:
        return self.session.query(Userdb).filter(Userdb.user_id==user_id).first()

    def get_userdb_from_token(self, token: str) -> Userdb | None:
        return self.session.query(Userdb).filter(Userdb.token==token).first()
    
    def delete_user(self, user_id: int) -> None:
        with self.lock:
            self.session.query(Userdb).filter(Userdb.user_id==user_id).delete()
        self.commit()

    # converters
    @staticmethod
    def user_from_userdb(user_db: Userdb) -> User:
        return User(user_db.user_id, user_db.username, user_db.email, user_db.publickey)

    @staticmethod
    def user_from_groupuserdb(groupuser_db: GroupUserdb) -> User:
        stored_user = DBManager.get_inst().get_userdb_from_id(groupuser_db.user_id)
        return DBManager.user_from_userdb(stored_user)

    @staticmethod
    def group_from_groupdb(group_db: Groupdb) -> Group:
        members = []
        for member in group_db.groupusers:
            members.append((DBManager.user_from_groupuserdb(member), member.isadmin))
        return Group(group_db.group_id, group_db.groupname, group_db.description, members)

    @staticmethod
    def message_from_messagedb(message_db: Messagedb) -> Message:
        sender = DBManager.user_from_userdb(DBManager.get_inst().get_userdb_from_id(message_db.sender_id))
        
        stored_group = DBManager.get_inst().get_groupdb_from_id(message_db.group_id)
        receiver = DBManager.group_from_groupdb(stored_group)
        if stored_group.is_privatechat:
            for member in receiver.members:
                if member[0].user_id != sender.user_id:
                    receiver = member[0]
        
        return Message(message_db.message_id, sender, receiver, message_db.content)
