from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.router import api_router
from database.postgresql import init_postgresql_db
from database.redis import close_redis
from exceptions.error_handlers import register_error_handlers
from taskiq_app import broker


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_postgresql_db()
    await broker.startup()
    yield
    await broker.shutdown()
    await close_redis()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
register_error_handlers(app)