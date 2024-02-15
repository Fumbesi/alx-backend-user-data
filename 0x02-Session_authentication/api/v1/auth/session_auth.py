#!/usr/bin/env python3
""" Module of Authentication
"""
import os
from flask import request
from typing import List, TypeVar
import uuid

class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if endpoint requires authentication."""
        if not path or not excluded_paths:
            return True

        normalized_path = path.rstrip('/') + '/'
        
        for exc in excluded_paths:
            normalized_exc = exc.rstrip('/')
            if not normalized_exc.endswith('*') and normalized_path == normalized_exc:
                return False
            elif normalized_exc.endswith('*') and normalized_path.startswith(normalized_exc[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Retrieve the authorization header from the Flask request."""
        if request:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Validate and return the current authenticated user."""
        # Implement user authentication logic here
        return authenticated_user

class SessionAuth(Auth):
    """ Class for session-based authentication """
    
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id."""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

if __name__ == "__main__":
    # Switch between Auth and SessionAuth based on environment variable
    if os.environ.get("AUTH_TYPE") == "session_auth":
        AuthClass = SessionAuth
    else:
        AuthClass = Auth

    # Now use AuthClass as your authentication class
    auth_instance = AuthClass()

    # Validate inheritance
    path = "/api/resource"
    excluded_paths = ["/api/public*", "/api/static*"]

    # Validate require_auth method
    requires_auth = auth_instance.require_auth(path, excluded_paths)
    print(f"Requires Authentication: {requires_auth}")

    # Validate authorization_header method
    fake_request = {'headers': {'Authorization': 'Bearer token'}}
    auth_header = auth_instance.authorization_header(request=fake_request)
    print(f"Authorization Header: {auth_header}")

    # Validate current_user method
    fake_user = auth_instance.current_user(request=fake_request)
    print(f"Current User: {fake_user}")

    # Validate SessionAuth create_session method
    session_auth = SessionAuth()
    user_id = None
    session = session_auth.create_session(user_id)
    print(f"{user_id} => {session}: {session_auth.user_id_by_session_id}")

    user_id = 89
    session = session_auth.create_session(user_id)
    print(f"{user_id} => {session}: {session_auth.user_id_by_session_id}")

    user_id = "abcde"
    session = session_auth.create_session(user_id)
    print(f"{user_id} => {session}: {session_auth.user_id_by_session_id}")

    user_id = "fghij"
    session = session_auth.create_session(user_id)
    print(f"{user_id} => {session}: {session_auth.user_id_by_session_id}")

    user_id = "abcde"
    session = session_auth.create_session(user_id)
    print(f"{user_id} => {session}: {session_auth.user_id_by_session_id}")