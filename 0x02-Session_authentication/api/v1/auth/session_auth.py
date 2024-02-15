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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

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

    # Validate SessionAuth create_session and user_id_for_session_id methods
    session_auth = SessionAuth()

    user_id_1 = "abcde"
    session_1 = session_auth.create_session(user_id_1)
    print(f"{user_id_1} => {session_1}: {session_auth.user_id_by_session_id}")

    user_id_2 = "fghij"
    session_2 = session_auth.create_session(user_id_2)
    print(f"{user_id_2} => {session_2}: {session_auth.user_id_by_session_id}")

    print("---")

    tmp_session_id = None
    tmp_user_id = session_auth.user_id_for_session_id(tmp_session_id)
    print(f"{tmp_session_id} => {tmp_user_id}")

    tmp_session_id = 89
    tmp_user_id = session_auth.user_id_for_session_id(tmp_session_id)
    print(f"{tmp_session_id} => {tmp_user_id}")

    tmp_session_id = "doesntexist"
    tmp_user_id = session_auth.user_id_for_session_id(tmp_session_id)
    print(f"{tmp_session_id} => {tmp_user_id}")

    print("---")

    tmp_session_id = session_1
    tmp_user_id = session_auth.user_id_for_session_id(tmp_session_id)
    print(f"{tmp_session_id} => {tmp_user_id}")

    tmp_session_id = session_2
    tmp_user_id = session_auth.user_id_for_session_id(tmp_session_id)
    print(f"{tmp_session_id} => {tmp_user_id}")

    print("---")

    session_1_bis = session_auth.create_session(user_id_1)
    print(f"{user_id_1} => {session_1_bis}: {session_auth.user_id_by_session_id}")

    tmp_user_id = session_auth.user_id_for_session_id(session_1_bis)
    print(f"{session_1_bis} => {tmp_user_id}")

    tmp_user_id = session_auth.user_id_for_session_id(session_1)
    print(f"{session_1} => {tmp_user_id}")
