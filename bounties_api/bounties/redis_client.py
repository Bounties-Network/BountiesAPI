import redis
from django.conf import settings

redis_client = redis.from_url(
    url=settings.REDIS_LOCATION
)
