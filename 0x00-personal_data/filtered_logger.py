#!/usr/bin/env python3

import re

def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in the log message using redaction.

    Args:
        fields (list): List of strings representing fields to obfuscate.
        redaction (str): String representing the redaction value.
        message (str): String representing the log line.
        separator (str): String representing the character separating fields in the log line.

    Returns:
        str: Obfuscated log message.
    """
    return re.sub(r'(?<=(' + '|'.join(fields) + r')=)[^' + re.escape(separator) + r']*',
                  redaction, message)
