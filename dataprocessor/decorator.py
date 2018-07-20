import time


def timer(func):
    def deco(*args, **kwargs):
        print(f'running func {func.__name__}')
        start = time.time()
        res = func(*args, **kwargs)
        stop = time.time()
        print(f'func "{func.__name__}" done, using {stop-start}s')
        return res
    return deco

