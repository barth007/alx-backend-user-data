#!/usr/bin/env python3
"""
filtered_logger.py
"""
from typing import List
import re
import logging
import csv


"""
reading a csv file and storing it's headers in
a constant
"""
path_file = 'user_data.csv'
with open(path_file) as csvfile:
    readerfile = csv.reader(csvfile)
    header = tuple(next(readerfile))
    PII_FIELDS = header[1:6]


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
