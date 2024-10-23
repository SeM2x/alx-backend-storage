#!/usr/bin/env python3
import requests
import redis
from typing import Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method using Redis.
    """
    @wraps(method)
    def inc(url) -> Any:
        """
        Increments the value of a Redis key and then calls the given method.
        """
        key = f"count:{url}"
        redis.Redis().incr(key)
        expiration_time = 10
        redis.Redis().expire(key, expiration_time)
        return method(url)
    return inc


@count_calls
def get_page(url: str) -> str:
    """
    Fetches the content of the given URL and returns it as a string.
    """
    response = requests.get(url)
    return response.text
