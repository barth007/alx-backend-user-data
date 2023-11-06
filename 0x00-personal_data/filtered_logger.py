#!/usr/bin/env python3
"""
filtered_logger.py
"""
from os import environ
from typing import List
import re
import logging
import mysql.connector


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


def get_db() -> mysql.connector.connect:
    """
    creating a connector to a database
    """

    try:
        config = {
            'user': environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
            'password': environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
            'host': environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
            'database': environ.get('PERSONAL_DATA_DB_NAME'),
        }
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def main() -> None:
    """
    calling a logger for a retrieve data
    """

    db = get_db()
    cursor = db.cursor()
    query = ("SELECT * FROM users")

    cursor.execute(query)
    result = cursor.fetchall()
    logger = get_logger()
    message = 'name={}; email={}; phone={}; ssn={}; password={}; ip={};\
            last_login={}; user_agent={};'
    for (
            name,
            email,
            phone,
            ssn,
            password,
            ip,
            last_login,
            user_agent
            ) in result:
        logger.info(message.format(
                        name,
                        email,
                        phone,
                        ssn,
                        password,
                        ip,
                        last_login,
                        user_agent
                    ))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
