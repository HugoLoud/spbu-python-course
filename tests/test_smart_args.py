# tests/test_smart_args.py

import pytest
from project.smart_args import smart_args, Evaluated, Isolated
import random


def test_smart_args_evaluated():
    """
    Test using Evaluated for deferred computation of default values.
    """
    def get_random_number():
        return random.randint(0, 100)

    @smart_args()
    def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
        return (x, y)

    x1, y1 = check_evaluation()
    x2, y2 = check_evaluation()
    x3, y3 = check_evaluation(y=150)

    assert x1 == x2  # x should be the same, since it's computed at definition time
    assert y1 != y2  # y should be different, as it's evaluated at call time
    assert y3 == 150  # y is explicitly provided


def test_smart_args_isolated():
    """
    Test using Isolated for deep copying arguments.
    """
    @smart_args()
    def check_isolation(*, d=Isolated()):
        d['a'] = 0
        return d

    no_mutable = {'a': 10}
    result = check_isolation(d=no_mutable)

    assert result == {'a': 0}
    assert no_mutable == {'a': 10}  # Original object should not be modified


def test_smart_args_isolated_argument_required():
    """
    Test that an argument with Isolated is required.
    """
    @smart_args()
    def check_isolation(*, d=Isolated()):
        return d

    with pytest.raises(TypeError):
        check_isolation()  # Argument 'd' is required


def test_smart_args_combined_evaluated_isolated_error():
    """
    Test error when using Evaluated and Isolated together on the same parameter.
    """
    with pytest.raises(ValueError):
        @smart_args()
        def func(*, x=Evaluated(lambda: 1) and Isolated()):
            pass

    # Alternatively, create a class that inherits from both Evaluated and Isolated
    class EvalAndIso(Evaluated, Isolated):
        pass

    with pytest.raises(ValueError):
        @smart_args()
        def func_with_both(*, x=EvalAndIso(lambda: 1)):
            pass


def test_smart_args_positional_argument_error():
    """
    Test error when using Evaluated or Isolated with positional arguments.
    """
    with pytest.raises(ValueError):
        @smart_args()
        def func(x=Evaluated(lambda: 1)):
            pass


def test_smart_args_regular_default_value():
    """
    Test working with regular default values.
    """
    @smart_args()
    def func(*, x=10):
        return x

    assert func() == 10
    assert func(x=5) == 5


def test_smart_args_positional_support():
    """
    Test support for positional arguments when positional_support is enabled.
    """
    @smart_args(positional_support=True)
    def test_func(a=Evaluated(lambda: 10), b=Isolated()):
        b.append(a)
        return b

    # Test with 'a' using Evaluated default
    result = test_func(b=[1, 2])
    assert result == [1, 2, 10]

    # Test providing 'a' as a positional argument
    result = test_func(20, b=[1, 2])
    assert result == [1, 2, 20]


def test_smart_args_positional_evaluated():
    """
    Test using Evaluated with positional arguments.
    """
    @smart_args(positional_support=True)
    def func(a=Evaluated(lambda: 5)):
        return a

    assert func() == 5
    assert func(10) == 10


def test_smart_args_evaluated_not_overwritten():
    """
    Test that provided arguments are not overwritten by defaults.
    """
    def get_random_number():
        return random.randint(0, 100)

    @smart_args()
    def check_evaluation(*, y=Evaluated(get_random_number)):
        return y

    # Call with y provided
    assert check_evaluation(y=20) == 20

    # Call without y, should be computed
    result = check_evaluation()
    assert isinstance(result, int)


def test_smart_args_isolated_with_positional_support():
    """
    Test using Isolated with positional arguments when positional_support is enabled.
    """
    @smart_args(positional_support=True)
    def func_list(b=Isolated()):
        b.append(100)
        return b

    original_list = [1, 2]
    result = func_list(original_list)
    assert result == [1, 2, 100]
    assert original_list == [1, 2]  # Original list should not be modified
