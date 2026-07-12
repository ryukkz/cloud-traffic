from .redis_client import redis_client
LIMIT = 10
WINDOW = 60
class RateLimiter:
    def allow_request(self,client_id):
        key = f"rate_limit:{client_id}"

        current = redis_client.incr(key)

        if current == 1:
            redis_client.expire(key, WINDOW)

        if current > LIMIT:
            return False

        return True
