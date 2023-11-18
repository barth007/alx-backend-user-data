#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


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
            raise ValueError (f"User {email} already exits")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
