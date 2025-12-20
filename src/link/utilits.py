import string
from secrets import choice
import hashlib

from fastapi_cache.backends import redis

ALPHABET: str = string.ascii_letters + string.digits
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def generate_random_short_url() -> str:
    slug = ""
    for _ in range(6):
        slug += choice(ALPHABET)
    return slug


def hash_url(url: str) -> str:
    url = url.lower().strip()
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    if url.startswith('www.'):
        url = url[4:]

    return hashlib.md5(url.encode()).hexdigest()