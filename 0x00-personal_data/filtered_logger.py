#!/usr/bin/env python3

""" A function filter_datum that
    returns the log message
"""

import logging
import csv
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")  # Replace with the appropriate PII fields

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format Function """
        record.msg = self.filter_datum(self.fields, self.REDACTION,
                                       record.msg, self.SEPARATOR)
        return super().format(record)

    @staticmethod
    def filter_datum(fields: List[str], redaction: str,
                     message: str, separator: str) -> str:
        """ Obfuscate specified fields in the log message using redaction """
        return re.sub(rf"({'|'.join(fields)})=.*?{separator}",
                      rf"\1={redaction}{separator}", message)

def get_logger() -> logging.Logger:
    """ Return a configured logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a connector to the database """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connector

def main() -> None:
    """ Retrieve all rows in the users table and display each row under a filtered format """
    logger = get_logger()
    db = get_db()

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    
    for row in cursor:
        logger.info("name=%s; email=%s; phone=%s; ssn=%s; password=%s; ip=%s; last_login=%s; user_agent=%s;",
                    row["name"], row["email"], row["phone"], row["ssn"], row["password"],
                    row["ip"], row["last_login"], row["user_agent"])

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
