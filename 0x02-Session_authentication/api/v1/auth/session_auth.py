#!/usr/bin/env python3
""" Module of Authentication
"""
import os
from flask import request
from typing import List, TypeVar
import uuid
from models.user import User  # Assuming User is defined in models.user

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

    def session_cookie(self, request=None):
        """ Return the value of the session cookie from the request """
        if request is None:
            return None

        session_cookie_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_cookie_name, None)

    def current_user(self, request=None) -> User:
        """Return a User instance based on a cookie value."""
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                # Assuming User.get() is a method to retrieve a User from the database
                return User.get(user_id)

        return None
