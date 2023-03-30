"""Module for managing the database"""

# pylint: disable=E0401, R0402

from threading import Lock
from typing import List

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from database.model import Base, User as Userdb, Group as Groupdb, GroupUser as GroupUserdb, \
                           PrivateMessage as PrivateMessagedb, GroupMessage as GroupMessagedb
from data_classes import User, Group, Message
from custom_logger import CustomLogger
logger = CustomLogger().setup()

# pylint: disable=R0801

class DBManager():
    """Class that manages the database"""

    def __init__(self):
        if DBManager.get_inst() is not None:
            print(DBManager.get_inst())
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

    def add_user(self, username, email, publickey, salt, hashed_pw) -> None:
        with self.lock:
            user_obj = Userdb(username=username, email=email, publickey=publickey, salt=salt, hashed_pw=hashed_pw)
            self.session.add(user_obj)
        self.commit()

    def commit(self) -> None:
        """Commits changes to database"""

        with self.lock:
            try:
                self.session.commit()
            except sqlalchemy.exc.IntegrityError:
                logger.debug("Committing database changes failed, rolling back")
                self.session.rollback()

    def get_userdb_from_email(self, email: str) -> Userdb | None:
        return self.session.query(Userdb).filter(Userdb.email==email).first()

    def get_userdb_from_id(self, user_id: int) -> Userdb | None:
        return self.session.query(Userdb).filter(Userdb.user_id==user_id).first()
