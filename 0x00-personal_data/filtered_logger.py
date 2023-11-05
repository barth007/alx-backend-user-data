#!/usr/bin/env python3
"""
filtered_logger.py
"""
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    finds a pattern of personal data and replaces it constant strings
    """

    for item in fields:
        message = re.sub(rf"{item}.[^\{separator}]*",
                         f"{item}={redaction}", message)
    return message
