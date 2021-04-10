"""
Decorate print() so that it raises an error after printing a cumulative total 
of 100 arguments, and demonstrate this restriction.
"""

import functools, builtins

def count(limit: int):
    # decorator that limits number of arguments
    def count_print(func):
        # decorator that retains state information
        @functools.wraps(func)
        def wrapper_count_print(*args, **kwargs):
            # innermost decorator that compares state to cumulative limit
            # before executing function
            if (wrapper_count_print.num_prints + len(args)) <= limit:
                # if total arguments plus cumulative state is less than or equal
                # to limit, process function and add arguments to state
                wrapper_count_print.num_prints += len(args)
                builtins.print(f"Call {wrapper_count_print.num_prints} of {func.__name__!r}")
                return func(*args, **kwargs)
            else:
                # process remaining arguments up until limit
                func(*args[:(limit - wrapper_count_print.num_prints)], **kwargs)
                # raise error if limit is reached
                raise RuntimeError("This time is not allowed. Limit reached.")
        # initialize state tracking variable
        wrapper_count_print.num_prints = 0
        return wrapper_count_print
    return count_print

@count(100)
def print(*args, **kwargs):
    # builtins use to avoid recursion of calling print on itself
    return builtins.print(*args, **kwargs)


if __name__=='__main__':
    # Decorator can be tested in python3 by importing count and print above,
    # and utilizing various print statements; otherwise, following tests 
    # can be applied
    # NOTE: State can be checked with builtins.print(print.num_prints)


    for i in range(75):
        print(i)

    print(1, 2, 3, 4, 5, 6, 7, 8, 9, ['a', 'b'])

    for j in range(5):
        print("howdy")

    for k in range(15):
        print(k)        # This should result in error at print of '10' (101 times)

