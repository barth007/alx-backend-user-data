#!/usr/bin/env python3
"""
encrypt_password.py
"""
from typing import Union
import bcrypt


def hash_password(password: str) -> Union[bytes, str]:
    """
    This function takes a string as argument,
    hash and return it hashed value
    """

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    return hashed
