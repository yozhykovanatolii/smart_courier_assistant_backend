from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from exceptions.error_handlers import register_error_handlers

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
    
app = FastAPI(lifespan=lifespan)
register_error_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}