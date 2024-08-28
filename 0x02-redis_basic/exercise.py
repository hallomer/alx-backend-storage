#!/usr/bin/env python3
"""
Module to handle basic Redis operations and tracking.
"""

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


# Task 2: Incrementing Values
def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.

    Args:
        method: The method to decorate.

    Returns:
        The wrapped method with call counting.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


# Task 3: Storing Lists
def call_history(method: Callable) -> Callable:
    """
    Decorator to store call history of a method.

    Args:
        method: The method to decorate.

    Returns:
        The wrapped method with call history storage.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, result)
        return result

    return wrapper


# Task 4: Retrieving Lists
def replay(method: Callable) -> None:
    """
    Display the call history of a method.

    Args:
        method: The method to replay.
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    call_count = 0
    if redis_store.exists(method.__qualname__) != 0:
        call_count = int(redis_store.get(method.__qualname__))

    print(f"{method.__qualname__} was called {call_count} times:")
    inputs = redis_store.lrange(input_key, 0, -1)
    outputs = redis_store.lrange(output_key, 0, -1)
    for inp, out in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            method.__qualname__,
            inp.decode("utf-8"),
            out.decode("utf-8"),
        ))


# Task 0: Writing Strings to Redis
class Cache:
    """Cache class to interact with Redis."""

    def __init__(self):
        """Initialize the Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key.

        Args:
            data: Data to store (str, bytes, int, float).

        Returns:
            str: Key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    # Task 1: Reading from Redis and Recovering Original Type
    def get(self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key: Key of the data to retrieve.
            fn: Optional function to convert data.

        Returns:
            The data in its original type or converted by fn.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieve a string from Redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis."""
        return self.get(key, lambda x: int(x))
