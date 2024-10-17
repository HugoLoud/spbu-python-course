# test_matrix_operations.py
import pytest
from matrix import (
    get_row_matrix,
    get_cols_matrix,
    sum_matrix,
    product_matrix,
    transponiruem_matrix
)

def test_get_row_matrix():
    assert get_row_matrix([[1, 2], [3, 4]]) == 2
    assert get_row_matrix([]) == 0
    with pytest.raises(ValueError):
        get_row_matrix(None)

def test_get_cols_matrix():
    assert get_cols_matrix([[1, 2], [3, 4]]) == 2
    assert get_cols_matrix([[]]) == 0
    with pytest.raises(ValueError):
        get_cols_matrix(None)

def test_sum_matrix():
    assert sum_matrix([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]
    assert sum_matrix([[0, 0]], [[0, 0]]) == [[0, 0]]
    with pytest.raises(ValueError):
        sum_matrix([[1, 2]], None)
    with pytest.raises(ValueError):
        sum_matrix([[1, 2]], [[1]])

def test_product_matrix():
    assert product_matrix([[1, 2]], [[3], [4]]) == [[11]]
    assert product_matrix([[1, 0], [0, 1]], [[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    with pytest.raises(ValueError):
        product_matrix([[1]], [[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        product_matrix(None, [[1]])

def test_transponiruem_matrix():
    assert transponiruem_matrix([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert transponiruem_matrix([]) == []
    with pytest.raises(ValueError):
        transponiruem_matrix(None)
