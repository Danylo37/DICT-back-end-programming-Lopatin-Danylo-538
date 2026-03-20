"""Template rendering helper — auto-injects session_user into every response."""

from typing import Optional
from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

templates = Jinja2Templates(directory="templates")


def render(
    request: Request,
    template_name: str,
    context: Optional[dict] = None,
) -> _TemplateResponse:
    """
    Render a Jinja2 template with the given context.
    Automatically injects session_user from the current session.
    """
    if context is None:
        context = {}

    return templates.TemplateResponse(template_name, {
        "request": request,
        "session_user": request.session.get("user"),
        **context,
    })
