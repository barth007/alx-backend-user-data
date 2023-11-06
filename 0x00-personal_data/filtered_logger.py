#!/usr/bin/env python3
"""
filtered_logger.py
"""
from os import getenv
from typing import List
import re
import logging
from mysql.connector import connection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filters values of incoming records
        """

        messages = filter_datum(
                self.fields,
                self.REDACTION,
                record.getMessage(),
                self.SEPARATOR
            )
        record.msg = messages
        return super().format(record)


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


def get_logger() -> logging.Logger:
    """
    creating and return a logger instance
    """

    user_data = logging.getLogger(__name__)
    user_data.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data.addHandler(stream_handler)
    user_data.propagate = False
    return user_data


def get_db() -> connection.MySQLConnection:
    """
    creating a connector to a database
    """

    try:
        config = {
            'user': getenv('PERSONAL_DATA_DB_USERNAME'),
            'password': getenv('PERSONAL_DATA_DB_PASSWORD'),
            'host': getenv('PERSONAL_DATA_DB_HOST'),
            'database': getenv('PERSONAL_DATA_DB_NAME'),
        }
        cnx = connection.MySQLConnection(**config)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
