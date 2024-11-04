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
        if not callable(func):
            raise TypeError("Evaluated expects a callable with no arguments.")
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

        for name, param in parameters.items():
            default = param.default

            # Check if both Evaluated and Isolated are used together for the same parameter
            if isinstance(default, Evaluated) and isinstance(default, Isolated):
                raise ValueError(f"Cannot use Evaluated and Isolated together for parameter '{name}'.")

            if not positional_support and param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
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
            # Do not apply_defaults() to determine which arguments were provided
            # Apply defaults manually
            for name, param in signature.parameters.items():
                default = defaults.get(name)

                if name in bound_args.arguments:
                    # Argument is provided by the user
                    if isinstance(default, Isolated):
                        # Deep copy the provided argument
                        bound_args.arguments[name] = copy.deepcopy(bound_args.arguments[name])
                    # If not Isolated, leave the argument as is
                else:
                    # Argument not provided; handle defaults
                    if isinstance(default, Evaluated):
                        # Compute the default value
                        bound_args.arguments[name] = default.func()
                    elif isinstance(default, Isolated):
                        # Argument is required
                        raise TypeError(f"Argument '{name}' is required.")
                    else:
                        # Use the regular default value
                        bound_args.arguments[name] = default

            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator
