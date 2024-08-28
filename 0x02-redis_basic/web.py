#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis connection
cache = redis.Redis(host='localhost', port=6379, db=0)


def cache_page(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        # Define cache key for the URL
        cache_key = f"count:{url}"

        # Increment the count for the URL
        cache.incr(cache_key)

        # Check if the page is already cached
        cached_page = cache.get(url)
        if cached_page:
            print(f"Cache hit for {url}")
            return cached_page.decode('utf-8')

        # If not cached, call the function to fetch the page
        print(f"Cache miss for {url}, fetching content...")
        page_content = func(url)

        # Cache the result with an expiration time of 10 seconds
        cache.setex(url, 10, page_content)

        return page_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetches the HTML content of a given URL."""
    response = requests.get(url)
    return response.text
