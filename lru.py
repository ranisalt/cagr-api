import collections
import functools
import typing


def lru_async(max_size: int=128):
    cache = collections.OrderedDict()

    def decorator(f):
        @functools.wraps(f)
        async def memoizer(*args, **kwargs):
            key = str((args, kwargs))
            try:
                result = cache.pop(key)
                cache[key] = result
            except KeyError:
                if len(cache) >= max_size:
                    cache.popitem(last=False)
                result = cache[key] = await f(*args, **kwargs)
            return result
        return memoizer
    return decorator
