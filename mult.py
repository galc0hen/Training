def least_common_multiple(big_num, small_num):
    count = 1
    while True:
        if (big_num * count)%small_num == 0:
            return big_num * count
        else:
            count+=1


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
print('least_common_multiple of {} and {} is {}'.format(big_num, small_num, least_common_multiple))