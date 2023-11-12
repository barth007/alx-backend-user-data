#!/usr/bin/env python3
"""
Session Auth Module
"""
from api.v1.auth.auth import Auth
from flask import request, abort
import uuid


class SessionAuth(Auth):
    """
    Session Auth Class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session

        argument
            user_id: str
        Return
            returns a session
        """

        if user_id is None:
            return None
        elif not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrieving user_id from session_id
        """

        if session_id is None:
            return None
        elif not isinstance(session_id, str):
            return None
        else:
            user_id = self.user_id_by_session_id.get(session_id)
            return user_id
