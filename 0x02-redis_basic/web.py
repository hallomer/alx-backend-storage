#!/usr/bin/env python3
"""
Module to implement a web cache with expiration using Redis.
"""

import requests
import redis
from typing import Callable


class WebCache:
    """WebCache class to cache web pages with expiration."""

    def __init__(self):
        """Initialize the Redis client."""
        self._redis = redis.Redis()

    def get_page(self, url: str) -> str:
        """
        Get HTML content of a URL, cache it, and track access count.

        Args:
            url: The URL to fetch.

        Returns:
            str: HTML content of the page.
        """
        key = f"count:{url}"
        self._redis.incr(key)
        cache_key = f"cache:{url}"
        content = self._redis.get(cache_key)

        if content is None:
            response = requests.get(url)
            content = response.text
            self._redis.setex(cache_key, 10, content)

        return content
