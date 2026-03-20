"""Authentication service — password hashing and session management."""

import hashlib
import os
from typing import Optional
from fastapi import Request


def hash_password(password: str) -> str:
    """Hash a plain-text password with a random salt using SHA-256."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, stored: str) -> bool:
    """Verify a plain-text password against a stored salt:hash string."""
    try:
        salt, hashed = stored.split(":")
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
    except Exception:
        return False


def get_current_user(request: Request) -> Optional[dict]:
    """Return the current user dict from session, or None if not logged in."""
    return request.session.get("user")


def login_user(request: Request, user: dict) -> None:
    """Save the user's id, name, and email to the session."""
    request.session["user"] = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
    }


def logout_user(request: Request) -> None:
    """Clear all data from the session."""
    request.session.clear()
