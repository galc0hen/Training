import time
from functools import partial


def timer(func):
    average_running_time = 0
    total_number_of_executions = 0
    while True:
        executions_counter = yield
        while executions_counter > 0:
            executions_counter -= 1
            total_number_of_executions += 1
            # Calculate execution time of function.
            time_before_execution = time.monotonic()
            func()
            time_after_execution = time.monotonic()
            # Calculate average execution time.
            current_execution_time = time_after_execution - time_before_execution
            average_running_time = ((average_running_time * (total_number_of_executions - 1)
                                     + current_execution_time)) / total_number_of_executions
        yield average_running_time


def my_slow_func(sleep_time):
    time.sleep(sleep_time)
    print('running slowly...')


partial_slow_func = partial(my_slow_func, 0.02)


def run_my_timer_generator(my_func_timer_generator, executions_number=1):
    next(my_func_timer_generator)
    print(my_func_timer_generator.send(executions_number))


def main():
    """
    Expected Output (execution times may slightly change):
        running slowly...
        0.015000000013969839
        running slowly...
        0.022999999986495823
        running slowly...
        running slowly...
        running slowly...
        running slowly...
        running slowly...
        0.020000000001995692
    """
    # Create generator.
    my_func_timer_generator = timer(partial_slow_func)
    # Run generator.
    run_my_timer_generator(my_func_timer_generator)
    run_my_timer_generator(my_func_timer_generator)
    run_my_timer_generator(my_func_timer_generator, 5)


if __name__ == '__main__':
    main()
