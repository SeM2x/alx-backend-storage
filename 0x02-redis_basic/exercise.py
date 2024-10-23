#!/usr/bin/env python3
"""
This module provides a Cache class for storing data in a Redis database.
"""
import redis
import uuid
from typing import Self, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """"""
    key = method.__qualname__

    @wraps(method)
    def inc(self, data):
        self._redis.incr(key)
        return method
    return inc


class Cache:
    """
    Cache class for storing data in Redis with unique keys.
    """

    def __init__(self: Self):
        """
        Initializes a new Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self: Self, data: str) -> bool:
        """
        Stores the given data in Redis with a unique key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self: Self, key: str, fn: Callable = None) -> bytes | str | int:
        """
        Retrieves data from Redis and applies an optional transformation function.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self: Self, key: str) -> str:
        """
        Retrieve a string value from Redis by key.
        """
        return self.get(key, str)

    def get_int(self: Self, key: str) -> int:
        """
        Retrieve an integer value from Redis by key.
        """
        return self.get(key, int)
