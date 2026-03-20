"""Database connection and initialization module."""

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from contextlib import contextmanager
from dotenv import load_dotenv
from typing import Generator
import mysql.connector
import time
import os

load_dotenv()


def get_db() -> PooledMySQLConnection | MySQLConnectionAbstract:
    """Create and return a new MySQL database connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@contextmanager
def get_cursor(dictionary: bool = False) -> Generator:
    """Context manager that yields a cursor and handles commit/cleanup."""
    db = get_db()
    cursor = db.cursor(dictionary=dictionary)
    try:
        yield cursor
        db.commit()
    finally:
        cursor.close()
        db.close()


def init_db() -> None:
    """
    Create all required tables if they don't exist.
    Retries up to 10 times if DB is not ready yet.
    """
    for attempt in range(10):
        try:
            with get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS User (
                        id                  INT AUTO_INCREMENT PRIMARY KEY,
                        email               VARCHAR(255) NOT NULL UNIQUE,
                        name                VARCHAR(100) NOT NULL,
                        password            VARCHAR(255) NOT NULL,
                        is_confirmed        TINYINT(1) NOT NULL DEFAULT 0,
                        confirmation_token  VARCHAR(64) DEFAULT NULL,
                        created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                        INDEX idx_user_email (email),
                        INDEX idx_user_token (confirmation_token)
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Comment (
                        id          INT AUTO_INCREMENT PRIMARY KEY,
                        user_id     INT NOT NULL,
                        text        TEXT NOT NULL,
                        date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,

                        INDEX idx_comment_user_id (user_id),
                        INDEX idx_comment_date (date)
                    )
                """)
            return
        except Exception as e:
            print(f"DB not ready (attempt {attempt + 1}/10): {e}")
            time.sleep(2)
    raise RuntimeError("Could not connect to the database after 10 attempts")

