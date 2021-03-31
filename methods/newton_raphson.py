from math import *
from timeit import default_timer

from numba import jit
from scipy.misc import derivative


def wrapper_printer(count=0, n=0, fXn=0, fpXn=0, error=0, mode='default'):
    if mode == 'default':
        print(f'I[{count:2}]: Xn = {n:.4f}, f(Xn) = {fXn:.4f}, '
                f'f\'(Xn) = {fpXn:.4f}, %e = ',
                end='------\n' if count == 0 else f'{error:.4f}%\n')
    elif mode == '0.0':
        print(f'\n\nSince {error:.4f}% = 0.0000%, Xn is the root')
    elif mode == 'converge':
        print(f'\n\nSince {fpXn:.4f} is converging, Xn is the root')


@jit(forceobj=True)
def newton_raphson(f, n):
    count = 0
    prev_n = 0
    condition = True

    while condition:
        fXn = f(n)
        fpXn = derivative(func=f, x0=n, dx=1e-5)
        error = abs(((n - prev_n)/n) * 100)
        wrapper_printer(count, n, fXn, fpXn, error)
        prev_n = n
        n = n - (fXn/fpXn)
        
        if isclose(round(error, 4), 0.0000, rel_tol=1e-4):
            wrapper_printer(error=error, mode='0.0')
            condition = False
        elif isclose(round(fpXn, 4), round(derivative(func=f, x0=n), 4), rel_tol=1e-4):
            wrapper_printer(fpXn=fpXn, mode='converge')
            condition = False
        if count == 10:
            condition = False

        count += 1
    return n


if __name__ == '__main__':
    while 1:
        fx = input('Formula >> ')

        if fx.lower() == 'exit':
            print('Exiting...')
            break

        formula = lambda x: eval(fx)
        n = float(input('Xn >> '))

        try:
            print('\n\nITERATION:')
            start = default_timer()
            print(f'The root is: {newton_raphson(formula, n):.4f}\n')
            print(f'Computation took {round(default_timer() - start, 3)} ',
                end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
        except ZeroDivisionError as ex:
            print(f'There is a problem. ERROR: {ex}')
        finally:
            print('----------------------------------------------------------------\n')