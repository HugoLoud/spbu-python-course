"""
This module contains generator functions for RGBA vectors and prime numbers.
"""

from typing import Generator, Tuple


def get_rgba(i: int) -> Tuple[int, int, int, int]:
    """
    Returns the i-th RGBA vector in a four-dimensional set where:
    - R, G, B values range from 0 to 255 inclusive.
    - A (transparency) takes even values from 0 to 100 inclusive.

    Parameters:
        i (int): The index of the RGBA vector to retrieve.

    Returns:
        Tuple[int, int, int, int]: A tuple representing the (R, G, B, A) values.

    Raises:
        IndexError: If the index i is out of bounds.
    """
    N_r = 256  # Number of possible R values (0-255)
    N_g = 256  # Number of possible G values (0-255)
    N_b = 256  # Number of possible B values (0-255)
    N_a = 51   # Number of possible A values (0-100, even numbers only)

    total_N = N_r * N_g * N_b * N_a  # Total number of RGBA combinations

    if i < 0 or i >= total_N:
        raise IndexError(f"Index {i} is out of bounds (0 to {total_N - 1})")

    # Calculate indices for A, B, G, R
    N_rgb = N_r * N_g * N_b  # Total combinations of RGB

    a_index = i // N_rgb
    rem = i % N_rgb

    b_index = rem // (N_r * N_g)
    rem = rem % (N_r * N_g)

    g_index = rem // N_r
    r_index = rem % N_r

    # Map indices to actual values
    r = r_index
    g = g_index
    b = b_index
    a = a_index * 2  # Even transparency values from 0 to 100

    return (r, g, b, a)


def primes() -> Generator[int, None, None]:
    """
    Generator function that yields an infinite sequence of prime numbers
    using the Sieve of Eratosthenes algorithm.

    Yields:
        int: The next prime number in the sequence.
    """
    D = {}  # Dictionary for marking multiples
    q = 2   # Starting integer to test for primality

    while True:
        if q not in D:
            # q is a new prime
            yield q
            D[q * q] = [q]  # Mark the square of q
        else:
            # q is composite, mark its multiples
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]  # Remove q from the dictionary
        q += 1  # Move to the next integer
