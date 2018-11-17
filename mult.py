def smallest_dividend(num_1, num_2):
    """
    Smallest dividend is defined here
    as the smallest number that can be divided
    by both num_1 and num_2.
    E.g.,
    3, 5 -> 15
    2, 4 -> 4
    8, 12 -> 24
    """
    big_num = max(num_1, num_2)
    small_num = min(num_1, num_2)
    counter = 1
    while True:
        if (big_num * counter) % small_num == 0:
            return big_num * counter
        counter += 1


def print_result(num_1, num_2, result):
    print(f'The smallest dividend of {num_1} and {num_2} is {result}')


def main():
    print_result(3, 5, smallest_dividend(3, 5))  # Result is 15.
    print_result(2, 4, smallest_dividend(2, 4))  # Result is 4.
    print_result(8, 12, smallest_dividend(8, 12))  # Result is 24.


if __name__ == '__main__':
    main()
