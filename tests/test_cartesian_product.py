from project.cartesian_product import cartesian_product_sum


def test_cartesian_product_complex_case():
    """
    Test the Cartesian product sum for a more complex case with larger integers.
    """
    lists = [[100, 200], [300, 400], [500, 600]]
    result = cartesian_product_sum(lists)
    # (100+300+500) + (100+300+600) + (100+400+500) + ... + (200+400+600)
    # Manually calculated result: 900 + 1000 + 1000 + 1100 + 1000 + 1100 + 1100 + 1200 = 8400
    assert result == 8400


def test_cartesian_product_with_large_numbers():
    """
    Test the Cartesian product sum with large numbers to verify it handles big integers.
    """
    lists = [[10000, 20000, 30000], [40000, 50000], [60000]]
    result = cartesian_product_sum(lists)
    # (10000+40000+60000) + (10000+50000+60000) + (20000+40000+60000) + ...
    # Manually calculated result: 110000 + 120000 + 120000 + 130000 + 130000 + 140000 = 750000
    assert result == 750000


def test_cartesian_product_with_negative_and_large_numbers():
    """
    Test the Cartesian product sum with a mix of large positive and negative numbers.
    """
    lists = [[-1000, 2000], [3000, -4000], [-5000, 6000]]
    result = cartesian_product_sum(lists)
    # (-1000+3000-5000) + (-1000+3000+6000) + (-1000-4000-5000) + (-1000-4000+6000) + ...
    # Manually calculated result: -3000 + 8000 - 10000 + 1000 - 7000 + 11000 + 4000 = 4000
    assert result == 4000


def test_cartesian_product_with_large_list_sizes():
    """
    Test the Cartesian product sum with larger list sizes to test scalability.
    """
    lists = [
        [i for i in range(100, 201, 50)],
        [j for j in range(500, 1001, 250)],
        [k for k in range(2000, 4001, 1000)],
    ]
    result = cartesian_product_sum(lists)
    # This will produce a large Cartesian product with 3 lists of different sizes.
    # We expect it to handle the increased computational load.
    # Result is pre-calculated manually to match expected sum of tuples.
    expected_result = 105300  # Pre-calculated manually.
    assert result == expected_result


def test_cartesian_product_with_empty_lists():
    lists = [[], [1, 2, 3], [4, 5]]
    result = cartesian_product_sum(lists)
    assert result == 0

def test_cartesian_product_with_non_integer_values():
    lists = [[1, 2], ["a", "b"], [3, 4]]
    try:
        result = cartesian_product_sum(lists)
        assert False, "Expected a TypeError"
    except TypeError:
        pass
