#!/usr/bin/env python3

import re
import logging


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        """
        constructor method
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in a log record
        """
        # NotImplementedError




def filter_datum(fields, redaction, message, separator):
    """Obfuscates the message logs

    Args:
        fields (list->str): names of diff fields
        redaction (str): _description_
        message (str): The log message
        separator (str): separator
    """
    for field in fields:
        result = re.sub(
                        field + '=*?'+separator,
                        field + '=' + redaction + separator, message)
    return result
