"""
Single entry point.
All routes are registered here and all requests pass through this file.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from controllers.home import router as home_router
from controllers.guestbook import router as guestbook_router
from controllers.auth import router as auth_router
from database import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize the database on startup."""
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(home_router)
app.include_router(guestbook_router)
app.include_router(auth_router)
