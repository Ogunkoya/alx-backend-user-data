#!/usr/bin/env python3
import logging
import csv
from typing import Tuple
import os
import mysql.connector
import logging

def filter_datum(fields, redaction, message, separator):
    '''
    '''
    regex_pattern = f'({re.escape(separator)}|^)({"|".join(map(re.escape, fields))})=([^{re.escape(separator)}]*)'
    return re.sub(regex_pattern, f'\\1\\2={redaction}', message)

class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    def __init__(self, fields: Tuple[str]):
        super().__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        for field in self.fields:
            message = message.replace(field, "********")
        return message

def get_logger() -> logging.Logger:
    '''
    function that takes no arguments and returns a logging.Logger object
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def get_db():
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    
    if not db_name:
        raise ValueError("Database name not provided in PERSONAL_DATA_DB_NAME environment variable.")
    
    db_connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    
    return db_connection

FILTERED_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']

def main():
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        filtered_row = filter_datum(FILTERED_FIELDS, '***', ';'.join(str(value) for value in row))
        logger.info(filtered_row)

    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()