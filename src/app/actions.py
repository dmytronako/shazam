from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import init_db


@asynccontextmanager
def lifespan(app: FastAPI):
    init_db()
    yield
