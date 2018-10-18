import functools

arguments_and_results = {}


def preprocessed_results(func):
    @functools.wraps(func)
    def wrapper_preprocessed_results(*args, **kwargs):
        kwargs_tuples = tuple(kwargs.items())  # convert dict to tuple to hash it
        arguments = args + kwargs_tuples
        if arguments not in arguments_and_results:
            result = func(*args, **kwargs)
            arguments_and_results[arguments] = result
        else:
            result = arguments_and_results[arguments]
        return result
    return wrapper_preprocessed_results


@preprocessed_results
def test_func(first_argument, second_argument, keyword_argument=None):
    return [first_argument, second_argument, keyword_argument]


print(arguments_and_results)
test_func(1, 2, keyword_argument=3)  # with kwarg
print(arguments_and_results)
test_func(0, 'a')  # without kwarg
print(arguments_and_results)
test_func(0, 'a')  # same arguments as last call
print(arguments_and_results)
