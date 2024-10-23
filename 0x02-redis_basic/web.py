#!/usr/bin/env python3
"""
This module provides a decorator to count method calls
using Redis and a function to fetch web page content.
"""
import requests
import redis
from typing import Callable, Any
from functools import wraps

redis_instance = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method using Redis.
    """
    @wraps(method)
    def inc(url) -> Any:
        """
        Increments the value of a Redis key and then calls the given method.
        """
        count_key = f"count:{url}"
        res_key = f"result:{url}"
        expiration_time = 10
        redis_instance.incr(count_key)
        if redis_instance.exists(res_key):
            return redis_instance.get(res_key).decode()
        res = method(url)
        redis_instance.set(res_key, res)
        redis_instance.expire(res_key, expiration_time)
        return res
    return inc


@count_calls
def get_page(url: str) -> str:
    """
    Fetches the content of the given URL and returns it as a string.
    """
    response = requests.get(url)
    return response.text
