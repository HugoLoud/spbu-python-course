from functools import wraps
from collections import OrderedDict
import json


def make_hashable(obj):
    """
    Converts an object into a hashable form.

    If the object is hashable, it returns it as is.
    Otherwise, it serializes the object into a JSON string.

    :param obj: The object to convert
    :return: A hashable object or its string representation
    """
    try:
        hash(obj)
        return obj
    except TypeError:
        # Serialize the unhashable object to a string
        return json.dumps(obj, sort_keys=True)


def cache_results(maxsize=0):
    """
    Decorator for caching function results.

    Caches the results of function calls based on the provided arguments.
    Supports limiting the cache size.

    :param maxsize: The maximum size of the cache (number of entries), default is 0 (caching disabled)
    :return: The decorator
    """
    def decorator(func):
        if maxsize <= 0:
            return func  # Caching not required

        cache = OrderedDict()  # Use OrderedDict to control insertion order

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper for the function that caches results.

            :param args: Positional arguments
            :param kwargs: Keyword arguments
            :return: The result of the function call
            """
            # Create a key based on the function arguments
            key_args = tuple(make_hashable(arg) for arg in args)
            key_kwargs = tuple(sorted((k, make_hashable(v)) for k, v in kwargs.items()))
            key = (key_args, key_kwargs)

            if key in cache:
                cache.move_to_end(key)
                return cache[key]

            # Call the original function and store the result
            result = func(*args, **kwargs)
            cache[key] = result

            # Control the cache size
            if len(cache) > maxsize:
                cache.popitem(last=False)  # Remove the oldest item

            return result

        return wrapper
    return decorator
