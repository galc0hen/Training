from collections import namedtuple
Pointer = namedtuple('Pointer', ['curr_pointer', 'max_pointer'])  # Using namedtuple for readability.


def _increase_pointers(pointers):
    for i in range(len(pointers)-1, -1, -1):  # Evaluate pointers from right to left.
        # Increase pointer.
        pointers[i] = Pointer(pointers[i].curr_pointer + 1, pointers[i].max_pointer)
        # Check if pointer is out of scope.
        # Never restart the first pointer.
        if pointers[i].curr_pointer < pointers[i].max_pointer or i == 0:
            break
        # If pointer is out of scope, restart it.
        pointers[i] = Pointer(0, pointers[i].max_pointer)


def _adjust_args(args, repeat):
    new_args = []
    for _ in range(repeat):
        new_args.append(args[0])
    return new_args


def product(*args, repeat=1):
    if repeat > 1:
        args = _adjust_args(args, repeat)
    result = []
    # List of pointers correlates to given list of arguments.
    pointers = [Pointer(0, len(iterable)) for iterable in args]
    while pointers[0].curr_pointer < pointers[0].max_pointer:
        for i in range(len(pointers)):
            curr_pointer = pointers[i].curr_pointer  # For readability.
            result.append(args[i][curr_pointer])
        yield(tuple(result))
        result = []
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
