from numpy import random, float32, mean
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


def time_fxn(f, X, y, bw, verbose=True, correct_answer=None):
    start = time.perf_counter()
    result = f(X, y, bw)
    end = time.perf_counter()
    if verbose:
        printout = f"{f.__name__}:\t{end-start}"
        if correct_answer is not None:
            acc = mean(100-100*(result - correct_answer)/correct_answer)
            printout += f'\t{acc}%'
        print(printout)
    return end-start, result


if __name__ == '__main__':
    import methods
    data = gen_data()
    times = {}
    times['numpy_for_loop'], correct_answer = time_fxn(methods.numpy_for_loop,*data)
    for f_name in methods.__all__[1:]:
        fxn = getattr(methods, f_name)
        times[f_name], _ = time_fxn(fxn, *data, correct_answer=correct_answer)
