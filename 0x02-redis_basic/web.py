#!/usr/bin/env python3
"""
This module provides a decorator to count method calls
using Redis and a function to fetch web page content.
"""
import requests
import redis
from typing import Callable
from functools import wraps


redis_instance = redis.Redis()


def cach_data(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method using Redis.
    """
    @wraps(method)
    def inc(url: str) -> str:
        """
        Increments the value of a Redis key and then calls the given method.
        """
        count_key = f"count:{url}"
        res_key = f"result:{url}"
        expiration_time = 10
        redis_instance.incr(count_key)
        res = redis_instance.get(res_key)
        if res:
            return res.decode('utf-8')
        res = method(url)
        redis_instance.set(count_key, 0)
        redis_instance.setex(res_key, expiration_time, res)
        return res
    return inc


@cach_data
def get_page(url: str) -> str:
    """
    Fetches the content of the given URL and returns it as a string.
    """
    response = requests.get(url)
    return response.text
