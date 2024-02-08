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

if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))
