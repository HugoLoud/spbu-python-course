def curry_explicit(func, arity):
    """
    Transforms a function into its curried form with the specified arity.

    Currying is the process of converting a function that takes multiple arguments
    into a sequence of functions, each taking a single argument.

    :param func: The original function to be curried
    :param arity: The arity of the function (number of expected arguments)
    :return: The curried function
    :raises ValueError: If arity is negative
    """

    if not isinstance(arity, int) or arity < 0:
        raise ValueError("Arity must be a non-negative integer.")

    def curried(*args):
        """
        Recursively collects arguments until the required arity is reached.

        :param args: Accumulated arguments
        :return: Either the next function to collect arguments or the result of calling the original function
        :raises TypeError: If too many arguments are provided
        """
        if len(args) > arity:
            raise TypeError(f"Expected {arity} arguments, got {len(args)}.")
        if len(args) == arity:
            return func(*args)
        # Return a new function expecting the next argument
        return lambda x: curried(*(args + (x,)))
    return curried


def uncurry_explicit(func, arity):
    """
    Transforms a curried function back into a regular function with the specified arity.

    :param func: The curried function to be uncurried
    :param arity: The arity of the function (number of expected arguments)
    :return: The uncurried function
    :raises ValueError: If arity is negative
    """

    if not isinstance(arity, int) or arity < 0:
        raise ValueError("Arity must be a non-negative integer.")

    def uncurried(*args):
        """
        Sequentially calls the curried function with each argument.

        :param args: Arguments for the uncurried function
        :return: The result of calling the original function
        :raises TypeError: If the number of arguments does not match the arity
        """
        if len(args) != arity:
            raise TypeError(f"Expected {arity} arguments, got {len(args)}.")
        result = func
        for arg in args:
            result = result(arg)
        return result
    return uncurried
