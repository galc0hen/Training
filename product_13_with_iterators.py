def _adjust_args(args, num_of_repeats):
    new_args = []
    for _ in range(num_of_repeats):
        new_args.append(args[0])
    return new_args


def _restart_iterator(iterators, args, iterator_pointer):
    iterators[iterator_pointer] = iter(args[iterator_pointer])


def product(*args, repeat=1):
    if repeat > 1:
        args = _adjust_args(args, repeat)
    result = []
    # List of iterators correlates to given list of arguments.
    iterators = [iter(iterable) for iterable in args]
    iterator_pointer = 0
    while True:
        try:
            next_element = next(iterators[iterator_pointer])
        except StopIteration:
            if iterator_pointer == 0:  # Never restart first iterator.
                break
            else:
                _restart_iterator(iterators, args, iterator_pointer)
                iterator_pointer -= 1
                continue
        try:
            result.pop(iterator_pointer)
        except IndexError:
            pass
        result.insert(iterator_pointer, next_element)
        iterator_pointer += 1
        if iterator_pointer == len(iterators):
            yield(tuple(result))
            iterator_pointer -= 1


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
