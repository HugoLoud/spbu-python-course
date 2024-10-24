import pytest
from vector import scalar_product, length_vec, cos_ab

def test_scalar_product():
    assert scalar_product([1, 2], [3, 4]) == 11
    assert scalar_product([-1, -2], [3, 4]) == -11
    assert scalar_product([0, 0], [0, 0]) == 0
    with pytest.raises(ValueError):
        scalar_product([1, 2], None)
    with pytest.raises(ValueError):
        scalar_product([1, 2], [3])

def test_length_vec():
    assert length_vec([0, 0], [3, 4]) == 5
    assert length_vec([1, 1], [4, 5]) == 5
    assert length_vec([1, 2], [1, 2]) == 0
    with pytest.raises(ValueError):
        length_vec(None, [1, 2])
    with pytest.raises(ValueError):
        length_vec([1, 2], [3])

def test_cos_ab():
    assert cos_ab([1, 0], [0, 1]) == 0
    assert cos_ab([1, 1], [1, 1]) == 1
    assert cos_ab([1, 2], [2, 1]) == 0.9999999999999999
    with pytest.raises(ValueError):
        cos_ab(None, [1, 2])
    with pytest.raises(ValueError):
        cos_ab([1, 2], [3])
    with pytest.raises(ValueError):
        cos_ab([0, 0], [1, 1])  # One vector is of length zero
