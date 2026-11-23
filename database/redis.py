from redis.asyncio import Redis
from config import settings

REDIS_URL = settings.cache_redis_url

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

async def get_redis() -> Redis:
    return redis_client

async def close_redis():
    await redis_client.aclose()