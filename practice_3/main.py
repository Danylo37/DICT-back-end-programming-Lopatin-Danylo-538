import re
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import csv
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

FILE = "comments.csv"
FIELDS = ["email", "name", "text"]
PAGE_SIZE = 3


def load_comments():
    comments = []

    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                comments.append(dict(row))

    return comments


def paginate_comments(page):
    all_comments = load_comments()
    total = len(all_comments)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PAGE_SIZE
    comments = all_comments[start: start + PAGE_SIZE]
    return comments, page, total_pages


def save_comment(data):
    write_header = not os.path.exists(FILE) or os.path.getsize(FILE) == 0
    with open(FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(data)


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
