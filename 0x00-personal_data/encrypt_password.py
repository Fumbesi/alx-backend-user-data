#!/usr/bin/env python3
"""
Encrypt Password module
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against its hashed version.

    Args:
        hashed_password (bytes): The salted, hashed password.
        password (str): The plain text password to be validated.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
