# Guestbook

A simple guestbook web application built with FastAPI and MySQL.  
Users can register, confirm their email, and leave comments.

## Stack

- **Python 3.11**, FastAPI, Jinja2
- **MySQL 8.0**
- **uv** — package manager
- **Docker** + Docker Compose

## Project Structure

```
controllers/   — route handlers (MVC Controller)
models/        — database queries (MVC Model)
services/      — auth, validation, email, templates
templates/     — HTML pages (MVC View)
database.py    — DB connection and table initialization
app.py         — single entry point
```

## Setup

**Requirements:** Docker and Docker Compose.

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in the values:
    ```
    DB_HOST=db
    DB_USER=app
    DB_PASSWORD=apppassword
    DB_NAME=app_db
    SECRET_KEY=your-secret-key
    EMAIL_SENDER=your@gmail.com
    EMAIL_PASSWORD=your_gmail_app_password
    BASE_URL=http://localhost:8000
    ```
   > For `EMAIL_PASSWORD` use a Gmail App Password, not your regular password.  
   > Generate one at: Google Account → Security → 2-Step Verification → App passwords

3. Start the application:
    ```bash
    docker-compose up --build
    ```

4. Open [http://localhost:8000](http://localhost:8000)

The database tables are created automatically on startup.

## Running without Docker

```bash
pip install uv
uv sync
uvicorn app:app --reload
```

Make sure MySQL is running and `.env` contains the correct `DB_HOST`.