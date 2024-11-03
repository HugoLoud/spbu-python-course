from project.cache_decorator import cache_results


def test_cache_caching():
    """
    Test caching of function results.
    """
    calls = []

    @cache_results(maxsize=2)
    def add(a, b):
        calls.append((a, b))
        return a + b

    assert add(1, 2) == 3
    assert add(1, 2) == 3  # Result should be cached
    assert add(2, 3) == 5
    assert add(1, 2) == 3  # Result should be recalculated (evicted from cache)
    assert len(calls) == 3  # Should have 3 function calls


def test_cache_no_caching():
    """
    Test when caching is disabled.
    """
    calls = []

    @cache_results(maxsize=0)
    def multiply(a, b):
        calls.append((a, b))
        return a * b

    assert multiply(2, 3) == 6
    assert multiply(2, 3) == 6
    assert len(calls) == 2  # Caching is disabled, function is called every time


def test_cache_unhashable_arguments():
    """
    Test caching functions with unhashable arguments.
    """
    calls = []

    @cache_results(maxsize=1)
    def concat_lists(a):
        calls.append(a)
        return a + [1]

    result1 = concat_lists([2])
    result2 = concat_lists([2])  # Should be cached
    assert result1 == [2, 1]
    assert result2 == [2, 1]
    assert len(calls) == 1  # Function called only once


def test_cache_keyword_arguments():
    """
    Test caching with keyword arguments.
    """
    calls = []

    @cache_results(maxsize=2)
    def greet(greeting, name):
        calls.append((greeting, name))
        return f"{greeting}, {name}!"

    assert greet(greeting="Hello", name="Alice") == "Hello, Alice!"
    assert greet(name="Alice", greeting="Hello") == "Hello, Alice!"  # Should be cached
    assert len(calls) == 1  # Function called only once


def test_cache_eviction():
    """
    Test eviction of old items from the cache when it overflows.
    """
    calls = []

    @cache_results(maxsize=2)
    def square(x):
        calls.append(x)
        return x * x

    assert square(2) == 4
    assert square(3) == 9
    assert square(4) == 16
    assert square(2) == 4  # Result should be recalculated
    assert len(calls) == 4  # Function called 4 times
