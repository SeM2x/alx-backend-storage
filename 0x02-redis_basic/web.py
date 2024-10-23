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


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_instance.incr(f'count:{url}')
        result = redis_instance.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_instance.set(f'count:{url}', 0)
        redis_instance.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Fetches the content of the given URL and returns it as a string.
    """
    response = requests.get(url)
    return response.text
