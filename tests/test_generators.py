"""
Tests for the get_rgba function.
"""

import pytest
from project.generators import get_rgba


def test_get_rgba():
    """
    Tests the get_rgba function for correctness and error handling.
    """
    N_r = 256
    N_g = 256
    N_b = 256
    N_a = 51  # Even values from 0 to 100 inclusive
    total_N = N_r * N_g * N_b * N_a

    # Test first element
    assert get_rgba(0) == (0, 0, 0, 0)

    # Test last element
    assert get_rgba(total_N - 1) == (255, 255, 255, 100)

    # Test a middle element
    mid_i = total_N // 2
    r, g, b, a = get_rgba(mid_i)
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    assert 0 <= a <= 100 and a % 2 == 0

    # Test IndexError for invalid indices
    with pytest.raises(IndexError, match="Index -1 is out of bounds"):
        get_rgba(-1)
    with pytest.raises(IndexError, match=f"Index {total_N} is out of bounds"):
        get_rgba(total_N)
