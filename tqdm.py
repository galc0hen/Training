from time import sleep
import datetime as dt
import sys


def Tqdm(iterable):
    iteration_counter = 1
    total_iterations = len(iterable)
    start_time = dt.datetime.now()
    for obj in iterable:
        # number of iteration
        sys.stdout.write('\rIteration {} of {}     '.format(iteration_counter, total_iterations))

        # elapsed time
        datetime_now = dt.datetime.now()
        curr_duration = datetime_now - start_time
        sys.stdout.write('elapsed time: {}     '.format(curr_duration))

        # iterations per second
        curr_duration_seconds = curr_duration.total_seconds()
        if curr_duration_seconds != 0:
            sys.stdout.write('iterations per second: {:.2f}     '.format(iteration_counter / curr_duration_seconds))
        else:
            sys.stdout.write('iterations per second: N/A     ')

        # Process Completion Percentage
        sys.stdout.write('Process Completion Percentage: {:.1%}     '.format(iteration_counter / total_iterations))

        # progress bar
        progress_bar_full = int((iteration_counter / total_iterations) * 10)
        progress_bar_empty = 10 - progress_bar_full
        progress_bar = '[' + '#' * progress_bar_full + ' ' * progress_bar_empty + ']'
        sys.stdout.write(progress_bar)

        # wrapping up
        sys.stdout.flush()
        iteration_counter += 1
        yield obj


for i in Tqdm(range(3)):
    sleep(3)
