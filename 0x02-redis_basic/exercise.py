#!/usr/bin/env python3
"""
This module provides a Cache class for storing data in a Redis database.
"""
import redis
import uuid
from typing import Callable, Any, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method using Redis.
    """
    key = method.__qualname__

    @wraps(method)
    def inc(self, *args, **kwargs) -> Any:
        """
        Increments the value of a Redis key and then calls the given method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return inc


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method in Redis.
    """
    inputs_key = method.__qualname__ + ":inputs"
    outputs_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def history(self, *args, **kwargs):
        """
        Store the input arguments and output of a method call in Redis.
        """
        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))
        return output
    return history


def replay(method: Callable) -> None:
    """
    Replays the history of calls to the given method,
    showing inputs and outputs.
    """
    key = method.__qualname__
    inputs_key = key + ":inputs"
    outputs_key = key + ":outputs"

    count = 0
    if redis.Redis().exists(key):
        count = int(redis.Redis().get(key))
    print(f'{key} was called {count} times:')
    inputs = redis.Redis().lrange(inputs_key, 0, -1)
    outputs = redis.Redis().lrange(outputs_key, 0, -1)
    for item in list(zip(inputs, outputs)):
        input = item[0].decode("utf-8")
        output = item[1].decode("utf-8")
        print(f'{key}(*{input}) -> {output}')


class Cache:
    """Represents an object for storing data in a Redis data storage.
    """

    def __init__(self) -> None:
        """Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in a Redis data storage and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, lambda x: int(x))
