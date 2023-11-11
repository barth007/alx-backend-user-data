#!/usr/bin/env python3
"""
Auth Module
"""
from flask import request
from typing import List, TypeVar


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
            if searched_path == path and (searched_path.endswith('/') or searched_path == path + '/'):
                    return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """authorized header
        """

        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """current requesting user
        """

        return request
