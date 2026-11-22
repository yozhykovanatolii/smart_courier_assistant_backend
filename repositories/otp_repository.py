from redis.asyncio import Redis

class OtpRepository:
    def __init__(self, redis: Redis, ttl_seconds: int = 300):
        self.__redis = redis
        self.__ttl = ttl_seconds
        
    async def save_opt_code(self, key: str, code: str) -> None:
        await self.__redis.set(name=key, value=code, ex=self.__ttl)

    async def consume_opt_code(self, key: str) -> str | None:
        return await self.__redis.getdel(name=key)