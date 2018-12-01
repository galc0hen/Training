import time


PADDING = f'\t\t'


def tqdm(iterable):
    iteration_counter = 1
    total_iterations = len(iterable)
    start_time = time.monotonic()
    for obj in iterable:
        # number of iteration
        tqdm_string_to_print = f'Iteration {iteration_counter} of {total_iterations}{PADDING}'

        # elapsed time
        time_now = time.monotonic()
        curr_duration = time_now - start_time
        tqdm_string_to_print += f'elapsed time: {curr_duration:.2f} sec {PADDING}'

        # iterations per second
        if curr_duration != 0:
            tqdm_string_to_print += f'iterations per second: ' \
                                    f'{iteration_counter / curr_duration:.2f}{PADDING}'
        else:
            tqdm_string_to_print += f'iterations per second: N/A{PADDING}'

        # Process Completion Percentage
        tqdm_string_to_print += f'Process Completion Percentage: {iteration_counter / total_iterations:.1%}{PADDING}'

        # progress bar
        progress_bar_full = int((iteration_counter / total_iterations) * 10)
        progress_bar_empty = 10 - progress_bar_full
        progress_bar = '[' + '#' * progress_bar_full + ' ' * progress_bar_empty + ']'
        tqdm_string_to_print += progress_bar

        # wrapping up
        print(end='\r')
        print(tqdm_string_to_print, end='')
        iteration_counter += 1
        yield obj


def main():
    """
    Expecting the following string structure:
    Iteration 5 of 5	elapsed time: 12.00 sec     iterations per second: 0.42    Process Completion Percentage: 100.0%   [##########]
    """
    for i in tqdm(range(5)):
        time.sleep(3)


if __name__ == '__main__':
    main()
