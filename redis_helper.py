import logging
import os

import redis

SESSION_MANAGER_KEY: str = 'SESSION_'

logger = logging.getLogger(__name__)


class RedisClient(object):
    def __init__(self, host=os.environ.get("REDIS_HOST"), port=int(os.environ.get("REDIS_PORT", 6379)),
                 db=os.environ.get("REDIS_DB"), password=os.environ["REDIS_PASSWORD"]):
        self.redis_client = redis.StrictRedis(host=host, port=port,
                                              db=db,
                                              password=password,
                                              decode_responses=True)

    def store_object(self, key, value):
        self.redis_client.set(key, value)
