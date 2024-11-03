import pytest
from project.curry import curry_explicit, uncurry_explicit


def test_curry_positive_arity():
    """
    Test currying a function with positive arity.
    """
    def f(x, y, z):
        return x + y + z

    f_curried = curry_explicit(f, 3)
    assert f_curried(1)(2)(3) == 6
    assert f_curried(1, 2, 3) == 6
    assert f_curried(1, 2)(3) == 6

    f_uncurried = uncurry_explicit(f_curried, 3)
    assert f_uncurried(1, 2, 3) == 6


def test_curry_zero_arity():
    """
    Test currying a function with arity 0.
    """
    def f():
        return 42

    f_curried = curry_explicit(f, 0)
    assert f_curried() == 42

    f_uncurried = uncurry_explicit(f_curried, 0)
    assert f_uncurried() == 42


def test_curry_one_arity():
    """
    Test currying a function with arity 1.
    """
    def f(x):
        return x * 2

    f_curried = curry_explicit(f, 1)
    assert f_curried(5) == 10

    f_uncurried = uncurry_explicit(f_curried, 1)
    assert f_uncurried(5) == 10


def test_curry_negative_arity():
    """
    Test handling of negative arity.
    """
    def f(x):
        return x

    with pytest.raises(ValueError):
        curry_explicit(f, -1)
    with pytest.raises(ValueError):
        uncurry_explicit(f, -1)


def test_curry_incorrect_arity():
    """
    Test handling of incorrect arity.
    """
    def f(x, y):
        return x + y

    f_curried = curry_explicit(f, 2)
    with pytest.raises(TypeError):
        f_curried(1)(2)(3)
    with pytest.raises(TypeError):
        f_curried(1, 2, 3)


def test_curry_variable_arity_function():
    """
    Test currying a function with variable arity.
    """
    def f(*args):
        return sum(args)

    f_curried = curry_explicit(f, 2)
    assert f_curried(1)(2) == 3
    with pytest.raises(TypeError):
        f_curried(1)(2)(3)
    with pytest.raises(TypeError):
        f_curried(1, 2, 3)

    f_uncurried = uncurry_explicit(f_curried, 2)
    assert f_uncurried(1, 2) == 3
