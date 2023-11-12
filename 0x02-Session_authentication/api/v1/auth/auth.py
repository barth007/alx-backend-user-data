#!/usr/bin/env python3
"""
Auth Module
"""
from flask import request
from typing import List, TypeVar
from os import environ


class Auth():
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth
        """

        if not excluded_paths or excluded_paths is None:
            return True
        elif path is None:
            return True
        for searched_path in excluded_paths:
            if searched_path == path or (searched_path.endswith('/')
               and searched_path == path + '/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorized header
        """

        if request is None:
            return request
        elif "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current requesting user
        """

        return None

    def session_cookie(self, request=None):
        """
        retrieving cookie session
        """

        if request is None:
            return None
        else:
            env_value = environ.get("SESSION_NAME")
            cookie_data = request.cookies.get(env_value)
            return cookie_data
