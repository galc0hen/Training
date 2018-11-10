import functools

arguments_to_results_map = {}


def preprocessed_results(func):
    """
    Map result to arguments to avoid running a function with same arguments twice.
    """

    @functools.wraps(func)
    def wrapper_preprocessed_results(*args, **kwargs):
        # Convert args and kwargs to tuple to hash them.
        sorted_kwargs = {}
        for key in sorted(kwargs.keys()):
            sorted_kwargs[key] = kwargs[key]
        kwargs_tuple = tuple(sorted_kwargs.items())
        arguments = args + kwargs_tuple
        # Check if arguments are preprocessed.
        if arguments in arguments_to_results_map:
            result = arguments_to_results_map[arguments]
        else:
            result = func(*args, **kwargs)
            arguments_to_results_map[arguments] = result
        return result
    return wrapper_preprocessed_results


@preprocessed_results
def test_func(first_argument, second_argument, kw_argument_1=None, kw_argument_2=None):
    return [first_argument, second_argument, kw_argument_1, kw_argument_2]


def main():
    print(arguments_to_results_map)  # Expecting empty dictionary (no function processed).
    test_func(1, 2, kw_argument_1=1, kw_argument_2=2)  # First run with kwarg.
    print(arguments_to_results_map)  # Expecting one item in dict.
    test_func(1, 2, kw_argument_2=2, kw_argument_1=1)  # Second run ith same kwargs inserted in different order.
    print(arguments_to_results_map)  # Expecting one item in dict (same as before).
    test_func(0, 'a')  # Without kwarg.
    print(arguments_to_results_map)  # Expecting two items in dict.
    test_func(0, 'a')  # Same arguments as last call of test_func.
    print(arguments_to_results_map)  # Expecting two items in dict (same as before).


main()
