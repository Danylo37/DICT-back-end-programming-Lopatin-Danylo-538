"""User model — handles all DB operations for the User table."""

from typing import Optional
from database import get_cursor


class UserModel:
    """Encapsulates all database queries for the User table."""

    @staticmethod
    def find_by_email(email: str) -> Optional[dict]:
        """Find and return a user by email, or None if not found."""
        with get_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
            return cursor.fetchone()

    @staticmethod
    def find_by_token(token: str) -> Optional[dict]:
        """Find a user by their confirmation token."""
        with get_cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT * FROM User WHERE confirmation_token = %s",
                (token,)
            )
            return cursor.fetchone()

    @staticmethod
    def create(data: dict) -> None:
        """
        Insert a new unconfirmed user.
        Expects: email, name, password, confirmation_token.
        """
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO User (email, name, password, confirmation_token, is_confirmed)
                VALUES (%s, %s, %s, %s, 0)
                """,
                (data["email"], data["name"], data["password"], data["confirmation_token"]),
            )

    @staticmethod
    def confirm(token: str) -> None:
        """Mark user as confirmed and clear the token."""
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE User
                SET is_confirmed = 1, confirmation_token = NULL
                WHERE confirmation_token = %s
                """,
                (token,)
            )
