"""Auth controller — register, login, logout, email confirmation."""

import secrets
from fastapi import APIRouter, Request, Form
from starlette.responses import Response, RedirectResponse

from models.user import UserModel
from services.auth import hash_password, verify_password, login_user, logout_user
from services.email_confirmation import send_confirmation_email
from services.validation import validate_register, validate_login
from services.templates import render

router = APIRouter()


@router.get("/register")
def register_page(request: Request) -> Response:
    """Render the registration form."""
    return render(request, "register.html", {"errors": {}, "form_data": {}})


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(default=""),
    name: str = Form(default=""),
    password: str = Form(default=""),
    password_confirm: str = Form(default=""),
) -> Response:
    """
    Handle registration form submission.
    On success, creates the user and sends a confirmation email.
    """
    errors = validate_register(email, name, password, password_confirm)

    if not errors and UserModel.find_by_email(email.strip()):
        errors["email"] = "This email is already registered."

    if not errors:
        token = secrets.token_hex(32)

        UserModel.create({
            "email": email.strip(),
            "name": name.strip(),
            "password": hash_password(password),
            "confirmation_token": token,
        })

        try:
            send_confirmation_email(email.strip(), token)
        except Exception:
            # Email sending failed — still allow registration, user can re-request later
            pass

        return render(request, "register_success.html", {"email": email.strip()})

    return render(request, "register.html", {
        "errors": errors,
        "form_data": {"email": email, "name": name},
    })


@router.get("/confirm/{token}")
def confirm_email(request: Request, token: str) -> Response:
    """Confirm email address via token from the confirmation link."""
    user = UserModel.find_by_token(token)

    if not user:
        return render(request, "confirm_result.html", {
            "success": False,
            "message": "Invalid or expired confirmation link.",
        })

    UserModel.confirm(token)
    return render(request, "confirm_result.html", {
        "success": True,
        "message": "Your email has been confirmed! You can now log in.",
    })


@router.get("/login")
def login_page(request: Request) -> Response:
    """Render the login form."""
    return render(request, "login.html", {"errors": {}, "form_data": {}})


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(default=""),
    password: str = Form(default=""),
) -> Response:
    """
    Handle login form submission.
    On success, saves user to session and redirects to guestbook.
    """
    errors = validate_login(email, password)
    user = None

    if not errors:
        user = UserModel.find_by_email(email.strip())
        if not user or not verify_password(password, user["password"]):
            errors["general"] = "Invalid email or password."
        elif not user["is_confirmed"]:
            errors["general"] = "Please confirm your email before logging in."
            user = None

    if not errors:
        login_user(request, user)
        return RedirectResponse("/guestbook", status_code=303)

    return render(request, "login.html", {
        "errors": errors,
        "form_data": {"email": email},
    })


@router.get("/logout")
def logout(request: Request) -> RedirectResponse:
    """Clear the session and redirect to the home page."""
    logout_user(request)
    return RedirectResponse("/", status_code=303)
