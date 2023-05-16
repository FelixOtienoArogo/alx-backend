#!/usr/bin/env python3
"""BasicCache."""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Is a caching system."""

    def put(self, key, item):
        """Add an item in the cache."""
        if key is not None or item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key."""
        return self.cache_data.get(key, None)
