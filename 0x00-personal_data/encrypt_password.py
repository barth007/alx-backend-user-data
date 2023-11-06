#!/usr/bin/env python3
"""
encrypt_password.py
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function takes a string as argument,
    hash and return it hashed value
    """

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checking if password and hashed_password are both
    valid
    """

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
