from numpy import random, float32
import time
__all__ = [
    'gen_data',
    'time_fxn',
]


def gen_data(n=60000):
    X = random.random(n).astype(float32)
    y = 100.*X + 100. + random.random(n).astype(float32)
    bw = (X.max() - X.min())/100.
    return X, y, bw


def time_fxn(f, X, y, bw, verbose=True):
    start = time.perf_counter()
    f(X, y, bw)
    end = time.perf_counter()
    if verbose:
        print(f"{f.__name__}:\t{end-start}")
    return end-start


if __name__ == '__main__':
    import methods
    data = gen_data()
    for f_name in methods.__all__:
        fxn = getattr(methods, f_name)
        time_fxn(fxn, *data)
