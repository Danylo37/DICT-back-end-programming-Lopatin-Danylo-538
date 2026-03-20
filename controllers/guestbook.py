"""Guestbook controller — public comment feed and authenticated comment submission."""

from fastapi import APIRouter, Request, Form
from starlette.responses import Response, RedirectResponse

from models.comment import CommentModel
from services.auth import get_current_user
from services.validation import validate_comment
from services.templates import render

router = APIRouter()

PAGE_SIZE = 3


def paginate(comments: list, page: int) -> tuple[list, int, int]:
    """
    Slice comments list for the given page.
    Returns (page_items, current_page, total_pages).
    """
    total = len(comments)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PAGE_SIZE
    return comments[start:start + PAGE_SIZE], page, total_pages


@router.get("/guestbook")
def guestbook(request: Request, page: int = 1) -> Response:
    """Display paginated comments. Accessible to everyone."""
    comments = CommentModel.get_all()
    comments, page, total_pages = paginate(comments, page)

    return render(request, "index.html", {
        "comments": comments,
        "page": page,
        "total_pages": total_pages,
        "errors": {},
        "form_data": {},
    })


@router.post("/add")
async def add_comment(
    request: Request,
    text: str = Form(default=""),
    page: int = Form(1),
) -> Response:
    """
    Submit a new comment.
    Requires authentication — redirects to /login if not logged in.
    """
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)

    errors = validate_comment(text)

    if not errors:
        CommentModel.create({
            "user_id": user["id"],
            "text": text.strip(),
        })
        return RedirectResponse("/guestbook", status_code=303)

    comments = CommentModel.get_all()
    comments, page, total_pages = paginate(comments, page)

    return render(request, "index.html", {
        "comments": comments,
        "page": page,
        "total_pages": total_pages,
        "errors": errors,
        "form_data": {"text": text},
    })
