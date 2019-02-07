from collections import namedtuple
Pointer = namedtuple('Pointer', ['curr_pointer', 'max_pointer'])  # Using namedtuple for readability.


def _increase_pointers(pointers):
    # Restart pointer of right most iterable.
    pointers[-1] = Pointer(0, pointers[-1].max_pointer)
    for i in range(len(pointers)-2, -1, -1):  # Evaluate pointers starting from one before last, to first.
        pointers[i] = Pointer(pointers[i].curr_pointer + 1, pointers[i].max_pointer)
        if pointers[i].curr_pointer < pointers[i].max_pointer or i == 0:  # Never restart the first pointer.
            break
        # If pointer is out of scope too, restart it and continue to increase the pointer before it.
        pointers[i] = Pointer(0, pointers[i].max_pointer)


def _adjust_args(args, repeat):
    new_args = []
    for _ in range(repeat):
        new_args.append(args[0])
    return new_args


def helper_iterator(iterable):
    for item in iterable:
        yield item


def product(*args, repeat=1):
    if repeat > 1:
        args = _adjust_args(args, repeat)
    result = []
    # List of iterators correlates to given list of arguments.
    iterators = [helper_iterator(iterable) for iterable in args]
    while pointers[0].curr_pointer < pointers[0].max_pointer: # catch stopiteration
        # yield next for each iterator to build solution
        for i in range(len(pointers)):
            curr_pointer = pointers[i].curr_pointer  # For readability.
            result.append(args[i][curr_pointer])
        yield(tuple(result))
        result = []
        # Move pointer of right most iterable.
        # yield next for last iterator to catch stop iteration
        #
        pointers[-1] = Pointer(pointers[-1].curr_pointer + 1, pointers[-1].max_pointer)
        # Check if pointer of right most iterable is out of scope.
        if pointers[-1].curr_pointer >= pointers[-1].max_pointer:
            _increase_pointers(pointers)


def main():
    # Expected output: [(1, 'A', True), (1, 'A', False), (1, 'B', True),
    # (1, 'B', False), (2, 'A', True), (2, 'A', False), (2, 'B', True),
    # (2, 'B', False), (3, 'A', True), (3, 'A', False), (3, 'B', True), (3, 'B', False)]
    print(list(product([1, 2, 3], 'AB', [True, False])))
    # Expected output: [(1, 2), (1, 'A'), ('A', 2), ('A', 'A')]
    print(list(product(*product([1, 2], 'A'))))
    # Expected output: [(1, 1), (1, 2), (2, 1), (2, 2)]
    print(list(product([1, 2], repeat=2)))


if __name__ == '__main__':
    main()
