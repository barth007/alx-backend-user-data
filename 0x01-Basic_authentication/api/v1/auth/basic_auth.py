#!/usr/bin/env python3
"""
Basic Auth Model
"""
from api.v1.auth.auth import Auth
from flask import request, abort
from models.user import User
from models.base import Base
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """
    Basic Auth Class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        encoding strings
        """

        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        else:
            value = authorization_header[6:]
            return value

    def decode_base64_authorization_header(
         self, base64_authorization_header: str) -> str:
        """
        Decoding strings
        """

        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None
        try:
            decodes = base64.b64decode(base64_authorization_header)
            decoded = decodes.decode('utf-8')
            return decoded
        except UnicodeDecodeError as e:
            return None

    def extract_user_credentials(
         self, decoded_base64_authorization_header: str) -> (str, str):
        """
        getting users credentials
        """

        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            values = decoded_base64_authorization_header.split(':')
            return tuple(values)

    def user_object_from_credentials(
         self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """retrieving users credentials

        argument
            user_email: str,
            user_pwd: str
        Return:
             user instances that matches the argument
        """

        if user_email is None or not isinstance(user_email, str):
            return None
        elif user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({"email": user_email})
        if user_list is None:
            return None
        else:
            for user in user_list:
                if user.is_valid_password(user_pwd):
                    return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves credentials of current users

        argument
             current request object
        Return:
            user instances
        """

        auth = Auth()
        authorization = auth.authorization_header(request)
        print(authorization)
        extract_base64 = self.extract_base64_authorization_header(
            authorization
            )
        decoded = self.decode_base64_authorization_header(extract_base64)
        extract_users = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(
            extract_users[0],
            extract_users[1]
            )
        return user
