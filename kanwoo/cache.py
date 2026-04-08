from abc import ABC, abstractmethod
import redis
import datetime

class Cache(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def set(self, key, value, time):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def flush(self):
        pass



class RedisCache(Cache):
    def __init__(self, app=None):
        self.app = app
        self.redis_url = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.redis_url = app.config["CACHE_URI"]

        self.redis = redis.from_url(self.redis_url, decode_responses=True)

    def set(self, key: str, value: str, ttl):
        self.redis.set(key, value, ex=datetime.timedelta(seconds=ttl))

    def get(self, key: str):
        return self.redis.get(key)

    def flush(self):
        self.redis.flushdb()