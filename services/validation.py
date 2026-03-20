"""Validation service for all form fields."""

import re


def validate_comment(text: str) -> dict[str, str]:
    """
    Validate comment text.
    Returns a dict of field -> error message. Empty dict means valid.
    """
    errors: dict[str, str] = {}

    if len(text.strip()) < 3:
        errors["text"] = "Text must be at least 3 characters."
    elif len(text.strip()) > 1000:
        errors["text"] = "Text must be at most 1000 characters."

    return errors


def validate_register(
    email: str,
    name: str,
    password: str,
    password_confirm: str,
) -> dict[str, str]:
    """
    Validate registration form.
    Returns a dict of field -> error message. Empty dict means valid.
    """
    errors: dict[str, str] = {}

    if not email.strip():
        errors["email"] = "Email is required."
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors["email"] = "Invalid email."

    if len(name.strip()) < 2:
        errors["name"] = "Name must be at least 2 characters."

    if len(password) < 6:
        errors["password"] = "Password must be at least 6 characters."
    elif password != password_confirm:
        errors["password_confirm"] = "Passwords do not match."

    return errors


def validate_login(email: str, password: str) -> dict[str, str]:
    """
    Validate login form.
    Returns a dict of field -> error message. Empty dict means valid.
    """
    errors: dict[str, str] = {}

    if not email.strip():
        errors["email"] = "Email is required."

    if not password:
        errors["password"] = "Password is required."

    return errors
