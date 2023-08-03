#!/usr/bin/env python3

import re


PII_FIELDS = ("name", "email", "password")


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
