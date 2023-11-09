#!/usr/bin/env python3
"""
Basic Auth Model
"""
from api.v1.auth.auth import Auth
from flask import request


class BasicAuth(Auth):
    """
    Basic Auth Class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        extracting authorizaton header
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
