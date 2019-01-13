from time import sleep
from timeit import timeit


def timer(func):
    average_running_time = 0
    total_number_of_executions = 0
    executions_counter = yield
    if executions_counter is None:
        executions_counter = 1
    while executions_counter > 0:
        executions_counter -= 1
        total_number_of_executions += 1
        current_execution_time = yield(timeit(func, number=1))
        print(current_execution_time)
        average_running_time = ((average_running_time * (total_number_of_executions - 1)
                                 + current_execution_time)) / total_number_of_executions


def my_slow_func():
    sleep(0.001)


def main():
    my_timer_generator = timer(my_slow_func)
    next(my_timer_generator)
    print(my_timer_generator.send(1))


if __name__ == '__main__':
    main()
