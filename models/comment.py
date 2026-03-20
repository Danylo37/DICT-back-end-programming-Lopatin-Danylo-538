"""Comment model — handles all DB operations for the Comment table."""

from database import get_cursor


class CommentModel:
    """Encapsulates all database queries for the Comment table."""

    @staticmethod
    def get_all() -> list[dict]:
        """
        Return all comments ordered by date descending,
        joined with User to get author name and email.
        """
        with get_cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT
                    c.id,
                    c.user_id,
                    c.text,
                    c.date,
                    u.name,
                    u.email
                FROM Comment c
                JOIN User u ON c.user_id = u.id
                ORDER BY c.date DESC
            """)
            return cursor.fetchall()

    @staticmethod
    def create(data: dict) -> None:
        """
        Insert a new comment.
        Expects: user_id, text.
        """
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Comment (user_id, text) VALUES (%s, %s)",
                (data["user_id"], data["text"]),
            )

    @staticmethod
    def delete(comment_id: int) -> None:
        """Delete a comment by its ID."""
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM Comment WHERE id = %s", (comment_id,))
