def helper_iterator(iterable):
    for item in iterable:
        yield item


a = [1, 2, 3]

y = helper_iterator(a)

while next(y) is not StopIteration:
    print(next(y))
