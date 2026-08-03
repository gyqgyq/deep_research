"""异步 Redis 客户端。"""

from redis.asyncio import Redis

from app.core.settings import settings

redis_client: Redis = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)
