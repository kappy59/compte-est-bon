from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


totaltimeit_dict = {}


def totaltimeit(func):
    @wraps(func)
    def totaltimeit_wrapper(*args, **kwargs):
        global totaltimeit_dict
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        totaltimeit_dict[func] = total_time + totaltimeit_dict.get(func, 0.0)

        return result

    return totaltimeit_wrapper


def totaltimeit_dump():
    global totaltimeit_dict
    for func, total_time in totaltimeit_dict.items():
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
