"""
This module contains decorators for wrapping generator functions.
"""

from typing import Callable, TypeVar, Generator, List

T = TypeVar("T")


def non_decreasing_index(
    generator_func: Callable[[], Generator[T, None, None]]
) -> Callable[[int], T]:
    """
    Decorator that wraps a generator function and returns a function which,
    when called with an integer k, returns the k-th element from the generator.
    The function enforces that calls are made with non-decreasing indices.

    Parameters:
        generator_func (Callable[[], Generator[T, None, None]]): The generator function to wrap.

    Returns:
        Callable[[int], T]: A function that returns the k-th element from the generator.

    Raises:
        ValueError: If the input index k is less than the last requested index.
    """

    def wrapper() -> Callable[[int], T]:
        gen = generator_func()  # Initialize the generator
        cache: List[T] = []  # Cache to store generated elements
        last_k = 0  # Last requested index

        def inner(k: int) -> T:
            nonlocal last_k
            if k < last_k:
                raise ValueError(
                    f"Index {k} is less than the last requested index {last_k}. "
                    "Indices must be non-decreasing."
                )
            while len(cache) < k:
                # Generate and cache the next element
                cache.append(next(gen))
            last_k = k
            return cache[k - 1]  # Return the k-th element (1-based indexing)

        return inner

    return wrapper()
