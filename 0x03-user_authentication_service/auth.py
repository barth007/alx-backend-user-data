#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


def _generate_uuid() -> str:
    """
    generates a uuid and returns a str of it
    """
    uuid_str = str(uuid.uuid4())
    return uuid_str


def _hash_password(password: str) -> bytes:
    """Hashing of a password string

    Args:
    - password (str): password to be hashed
    Return:
    - hashed string
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Instanciating the DB() Class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registering a new user to the database

        Args:
        - email (str): user email
        - password (str): user password

        Return:
        - User object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exits")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks if the login details are correct
        """
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            check = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            return check
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """generates a seesion and returns its

        Args:
        - email (str)
        Return:
        - a string generated session
        """
        try:
            user = self._db.find_user_by(email=email)
            generate_uuid = _generate_uuid()
            id = user.id
            self._db.update_user(id, session_id=generate_uuid)
            return user.session_id
        except (NoResultFound or ValueError):
            return None
