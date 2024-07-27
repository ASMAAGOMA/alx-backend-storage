#!/usr/bin/env python3
"""
exercide module
"""

import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    increments the count
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_k = method.__qualname__ + ":inputs"
        output_k = method.__qualname__ + ":outputs"
        self._redis.rpush(input_k, str(args))
        out = method(self, *args, **kwargs)
        self._redis.rpush(output_k, str(out))
        return out
    return wrapper


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


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

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generating the rand key and returning the data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes, int, float, None]:
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
