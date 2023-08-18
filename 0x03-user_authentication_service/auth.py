#!/usr/bin/env python3
"""
a _hash_password method that takes in a password string arguments
and returns bytes.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Method that takes in a password string arguments
    and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generate a new UUID and return it as a string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.

        Args:
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            User: The User object for the new user.

        Raises:
            ValueError:
                If a user with the same email already exists in the database.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f'User {email} already exists.')

    def valid_login(self, email: str, password: str) -> bool:
        """_summary_

        Args:
            email (str): required
            password (str): required

        Returns:
            bool
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password)

    def create_session(self, email: str) -> str:
        """method. It takes an email string argument
        returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                user.session_id = session_id
                self._db._session.commit()
                return session_id
            else:
                raise ValueError

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """method that takes a single session_id string argument
        and returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """method that takes a single user_id integer argument
        and returns None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """method that takes an email string argument
        and returns the user’s reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                user.reset_token = reset_token
                self._db._session.commit()
                return reset_token
            else:
                raise ValueError
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """method that takes reset_token string argument
        and a password string argument and returns None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                user.hashed_password = hashed_password
                user.reset_token = None
                self._db._session.commit()
            else:
                raise ValueError
        except NoResultFound:
            raise ValueError
