"""
Tests for the non_decreasing_index decorator and prime number generator.
"""

import pytest
from project.generators import primes
from project.decorators import non_decreasing_index


@pytest.fixture
def prime_function():
    """
    Fixture that returns the decorated prime number function.
    """
    return non_decreasing_index(primes)


def test_get_prime(prime_function):
    """
    Tests that the prime function returns correct prime numbers.
    """
    f = prime_function
    assert f(1) == 2
    assert f(2) == 3
    assert f(3) == 5
    assert f(4) == 7
    assert f(5) == 11

    # Test repeated calls with the same index
    assert f(5) == 11

    # Test increasing index
    assert f(6) == 13


@pytest.mark.parametrize("sequence", [
    ([1, 1, 2, 3, 5]),
    ([2, 2, 3]),
    ([3, 3, 3]),
])
def test_non_decreasing_sequence(prime_function, sequence):
    """
    Tests that non-decreasing sequences of indices are accepted.
    """
    f = prime_function
    for k in sequence:
        f(k)  # Should not raise an error


@pytest.mark.parametrize("sequence", [
    ([3, 2]),
    ([5, 4, 6]),
    ([10, 9]),
])
def test_decreasing_sequence(prime_function, sequence):
    """
    Tests that decreasing sequences of indices raise ValueError.
    """
    f = prime_function
    with pytest.raises(ValueError, match="Indices must be non-decreasing"):
        for k in sequence:
            f(k)
