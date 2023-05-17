#!/usr/bin/python3
"""  Basic Cache """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ Class that inherits from BaseCaching and is a caching system
        This caching system doesn’t have limit """
    def put(self, key, item):
        """ Assign to the dictionary """
        if key and item:
            self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            key_list = list(self.cache_data.keys())
            self.cache_data.pop(key_list[-2])
            print(f"DISCARD: {key_list[-2]}")

    def get(self, key):
        """ Return the value linked to key"""
        if key is None or self.cache_data.get(key) is None:
            return None
        return self.cache_data.get(key)
