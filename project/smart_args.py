import functools
import inspect
import copy


class Evaluated:
    """
    Class for deferred evaluation of default argument values.

    Used in the @smart_args decorator to indicate arguments
    whose default value should be computed at function call time.
    """

    def __init__(self, func):
        """
        Initialize Evaluated.

        :param func: A zero-argument function that computes the default value
        """
        self.func = func


class Isolated:
    """
    Marker class for deep copying the provided argument.

    Used in the @smart_args decorator to indicate arguments
    that should be copied before being used in the function.
    """

    pass


def smart_args(positional_support=False):
    """
    Decorator for smart processing of function arguments.

    Analyzes the types of default argument values and, depending on that,
    copies and/or computes them before executing the function.

    :param positional_support: Support for positional arguments (False by default)
    :return: The decorator
    """

    def decorator(func):
        signature = inspect.signature(func)
        parameters = signature.parameters
        defaults = {}

        # Collect information about the function's parameters
        for name, param in parameters.items():
            default = param.default
            if isinstance(default, Evaluated) and isinstance(default, Isolated):
                raise ValueError(
                    f"Cannot use Evaluated and Isolated together for parameter '{name}'."
                )

            if not positional_support and param.kind == param.POSITIONAL_ONLY:
                if isinstance(default, (Evaluated, Isolated)):
                    raise ValueError(
                        f"Evaluated and Isolated are not supported for positional arguments '{name}'."
                    )

            defaults[name] = default

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper for the function that processes default arguments.

            :param args: Positional arguments
            :param kwargs: Keyword arguments
            :return: The result of the function call
            """
            bound_args = signature.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()

            for name, value in bound_args.arguments.items():
                default = defaults.get(name)
                if isinstance(default, Evaluated):
                    if name not in kwargs:
                        # Compute the value at call time
                        bound_args.arguments[name] = default.func()
                elif isinstance(default, Isolated):
                    if name not in kwargs:
                        raise TypeError(f"Argument '{name}' is required.")
                    # Deep copy the argument
                    bound_args.arguments[name] = copy.deepcopy(
                        bound_args.arguments[name]
                    )

            # Call the original function with processed arguments
            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper
    return decorator
