#!/usr/bin/env python3
"""
encrypt_password.py
"""

import bcrypt


def hash_password(password: str) -> bcrypt.hashpw:
    """
    This function takes a string as argument,
    hash and return it hashed value
    """

    passw = b"{password}"
    hashed = bcrypt.hashpw(passw, bcrypt.gensalt(14))
    return hashed
