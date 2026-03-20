"""Home controller — renders the landing page."""

from fastapi import APIRouter, Request
from starlette.responses import Response
from services.templates import render

router = APIRouter()


@router.get("/")
def home(request: Request) -> Response:
    """Render the home page."""
    return render(request, "home.html")
