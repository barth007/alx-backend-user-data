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
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def find_user_by(self, **kwargs) -> User:
        """Find a user by abitary key argument

        Args:
        - **kwargs: key, values pair

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

    def update_user(self, user_id: int, **kwargs) -> None:
        """update users by id

        Args:
        - user_id (int): user id
        - kwargs: key, value pairs
        Return:
        - User: updated user
        """
        try:
            user = self.find_user_by(id=user_id)
            for attr, value in kwargs.items():
                setattr(user, attr, value)
                # user.attr = value
            self._session.commit()
        except ValueError as e:
            self._session.rollback()
            raise e
