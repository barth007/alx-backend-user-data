#!/usr/bin/env python3
"""
Basic Auth Model
"""
from api.v1.auth.auth import Auth
from flask import request
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
        except base64.binascii.Error as e:
            return None
