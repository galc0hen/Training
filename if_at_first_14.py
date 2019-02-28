from random import randint
import logbook
import functools


def retry(func):
    @functools.wraps(func)
    def wrapper_retry():
        logbook.FileHandler('error_log').push_application()
        log = logbook.Logger('error_log')
        while True:
            try:
                func()
                break
            except AssertionError:
                log.exception()

    return wrapper_retry


@retry
def often_failing_func():
    random_num = randint(1, 10)
    print(f'random number is {random_num}')
    assert random_num == 1


def main():
    # Expected output: to screen - all the numbers that were generated until 1 is generated.
    # Log file created with all the assertion errors documented.
    often_failing_func()


if __name__ == '__main__':
        main()
