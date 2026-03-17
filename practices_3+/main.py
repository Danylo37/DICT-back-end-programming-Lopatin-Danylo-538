import re
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from contextlib import contextmanager

app = FastAPI()
templates = Jinja2Templates(directory="templates")

PAGE_SIZE = 3


def get_db():
    return mysql.connector.connect(
        host="db",
        user="app",
        password="apppassword",
        database="app_db"
    )


@contextmanager
def get_cursor(dictionary=False):
    db = get_db()
    cursor = db.cursor(dictionary=dictionary)
    try:
        yield cursor
        db.commit()
    finally:
        cursor.close()
        db.close()


def load_comments():
    with get_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM Comment ORDER BY date DESC")
        return cursor.fetchall()


def save_comment(data):
    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO Comment (email, name, text) VALUES (%s, %s, %s)",
            (data["email"], data["name"], data["text"])
        )


def paginate_comments(page):
    all_comments = load_comments()
    total = len(all_comments)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PAGE_SIZE
    comments = all_comments[start: start + PAGE_SIZE]
    return comments, page, total_pages


def validate_comment(email, name, text):
    errors = {}
    email = email.strip()
    name = name.strip()
    text = text.strip()

    if not email:
        errors["email"] = "Email is required."
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors["email"] = "Enter a valid email address."

    if not name:
        errors["name"] = "Name is required."
    elif len(name) < 2:
        errors["name"] = "Name must be at least 2 characters."
    elif len(name) > 100:
        errors["name"] = "Name must be at most 100 characters."

    if not text:
        errors["text"] = "Comment text is required."
    elif len(text) < 3:
        errors["text"] = "Comment must be at least 3 characters."
    elif len(text) > 1000:
        errors["text"] = "Comment must be at most 1000 characters."

    return errors


@app.get("/")
def home(request: Request, page: int = 1):
    comments, page, total_pages = paginate_comments(page)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "comments": comments,
            "page": page,
            "total_pages": total_pages,
            "errors": {},
            "form_data": {},
        }
    )


@app.post("/add")
async def add_comment(request: Request, email = Form(...), name = Form(...), text = Form(...), page = Form(1)):
    errors = validate_comment(email, name, text)

    if not errors:
        comment = {
            "email": email.strip(),
            "name": name.strip(),
            "text": text.strip(),
        }
        save_comment(comment)
        return RedirectResponse(f"/?page=1", status_code=303)

    comments, page, total_pages = paginate_comments(page)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "comments": comments,
            "page": page,
            "total_pages": total_pages,
            "errors": errors,
            "form_data": {"email": email, "name": name, "text": text},
        },
        status_code=422,
    )
