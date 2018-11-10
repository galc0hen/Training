def least_common_multiple(big_num, small_num):
    count = 1
    while True:
        if (big_num * count) % small_num == 0:
            return big_num * count
        else:
            count += 1


def main():
    # read numbers from user
    while True:
        try:
            a = int(input('enter first number\n'))
        except ValueError:
            print('enter valid input')
            continue
        else:
            break

    while True:
        try:
            b = int(input('enter second number\n'))
        except ValueError:
            print('enter valid input')
            continue
        else:
            break
    big_num = max(a, b)
    small_num = min(a,b)
    least_common_multiple = least_common_multiple(big_num, small_num)
    print(f'Least common multiplier of {big_num} and {small_num} is {least_common_multiple}')


main()
