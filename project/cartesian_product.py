import itertools
from concurrent.futures import ThreadPoolExecutor
from typing import List


def cartesian_product_sum(lists: List[List[int]]) -> int:
    """
    Calculates the sum of the Cartesian product of the given lists using ThreadPoolExecutor.

    This function generates the Cartesian product of the given integer lists and computes
    the sum of all elements in each tuple of the product. The computation is parallelized
    using a thread pool.

    Args:
        lists (List[List[int]]): A list of integer lists for which the Cartesian product will be computed.

    Returns:
        int: The total sum of all elements in the Cartesian product.

    Example:
        cartesian_product_sum([[1, 2], [3, 4]]) will compute the Cartesian product:
        (1,3), (1,4), (2,3), (2,4) and return 20, because (1+3) + (1+4) + (2+3) + (2+4) = 20.
    """
    # Create a thread pool executor to parallelize the computation
    with ThreadPoolExecutor() as executor:
        # Compute the Cartesian product
        cartesian_product = itertools.product(*lists)
        # Map each tuple in the product to the sum of its elements and sum them all
        result = sum(executor.map(sum, cartesian_product))
    return result
