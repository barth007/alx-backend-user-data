#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
        - email (str): Email address of the user
        - hashed_password (str): Hashed password of the user

        Returns:
        - User: Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: str) -> User:
        """Find a user by abitary key argument

        Args:
        - **kwargs (str): key, values pair

        Returns:
        - User: found user
        """
        try:
            query = self._session.query(User)
            query = query.filter_by(**kwargs)
            one_user = query.one()
            return one_user
        except(NoResultFound, InvalidRequestError) as e:
            self._session.rollback()
            raise e
