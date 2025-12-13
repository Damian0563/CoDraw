from django.conf import settings
import redis

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    # password=settings.REDIS_PASSWORD,
    decode_responses=True
)

def get_redis_client():
    return redis_instance