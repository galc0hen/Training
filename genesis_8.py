ENGLISH_DICTIONARY = 'test_dict'
EOF = ''


# Utility function.
def find_prefix(f, prefix):
    f.seek(0)
    is_found = False
    next_word = f.readline()
    while next_word != EOF:
        if next_word.startswith(prefix):
            is_found = True
            break
        next_word = f.readline()
    if is_found is False:
        next_word = 'Error: Not Found'
    return next_word


# Generator.
def dictionary(my_dictionary):
    with open(my_dictionary, 'r') as f:
        while True:
            prefix = yield
            # Yield next word if no prefix sent, else search file for prefix.
            if prefix == '':
                next_word = f.readline()
                # Go back to beginning of file if reached EOF.
                if next_word == EOF:
                    f.seek(0)
                    next_word = f.readline()
            else:
                next_word = find_prefix(f, prefix)
            yield(next_word.rstrip())


def main():
    my_dictionary = dictionary(ENGLISH_DICTIONARY)
    # Print "banana".
    next(my_dictionary)
    print(my_dictionary.send('b'))
    # Print "robot".
    next(my_dictionary)
    print(my_dictionary.send('ro'))
    # Print "mango".
    next(my_dictionary)
    print(my_dictionary.send('m'))
    # Print "monkey".
    next(my_dictionary)
    print(my_dictionary.send(''))
    # Print "Error: Not Found".
    next(my_dictionary)
    print(my_dictionary.send('foo'))
    # Print "apple".
    next(my_dictionary)
    print(my_dictionary.send(''))


if __name__ == '__main__':
    main()
