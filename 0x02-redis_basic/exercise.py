#!/usr/bin/env python3
"""
exercide module
"""

import uuid
import redis
from typing import Union, Callable, Optional


class Cache:
    """
    the cache module
    """
    def __init__(self) -> None:
        """
        initialize _redis and flush db
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generating the rand key and returning the data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable]) -> Union[str, bytes, int, float, None]:
        """
        getting data in the desired format
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        string format
        """
        def sformatinng(data: bytes) -> str:
            """
            returning string
            """
            return data.decode('utf-8')
        return self.get(key, fn=sformatinng)

    def get_int(self, key: str) -> Optional[int]:
        """
        int format
        """
        def tformating(data: bytes) -> int:
            """
            returning int
            """
            return int(data)
        return self.get(key, fn=tformating)
