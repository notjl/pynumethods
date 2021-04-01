from math import *
from timeit import default_timer

from numba import jit
from scipy.misc import derivative
from tabulate import tabulate
from error_handler import InfiniteIteration

headers = ['[I]', 'Xn', 'f(Xn)', 'f\'(Xn)', '%e']
floatformat = (None, '.4f', '.4f', '.4f', '.4f')


def wrapper_printer(count=0,fpXn=0, error=0, mode='default'):
    if mode == 'default':
        print(f'\n\nSince {error:.4f}% = 0.0000%, Xn is the root')
    elif mode == 'converge':
        print(f'\n\nSince {fpXn:.4f} is converging , Xn is the root')
    elif mode == 'infinite' or mode == 'indefinite':
        print(f'\n\nSince I[{count}] >= 99, it is assumed it as an indefinite function.')
        print('Resulting in no definite or approximite root.')
        print('Re-check the function if it is correct.\n')


@jit(forceobj=True)
def newton_raphson(f, n):
    data = []
    count = 0
    prev_n = 0
    condition = True

    while condition:
        row = [count]
        fXn = f(n)
        fpXn = derivative(func=f, x0=n, dx=1e-5)
        error = abs(((n - prev_n)/n) * 100)

        row.extend([n, fXn, fpXn, round(error, 4) if count > 0 else None])
        data.append(row)

        prev_n = n
        n = n - (fXn/fpXn)
        
        if isclose(round(error, 4), 0.0000, rel_tol=1e-4):
            print(tabulate(data, headers=headers, floatfmt=floatformat,
                tablefmt='fancy_grid'))
            wrapper_printer(error=error)
            condition = False
        elif isclose(round(fpXn, 4), round(derivative(func=f, x0=n), 4), rel_tol=1e-4):
            print(tabulate(data, headers=headers, floatfmt=floatformat,
                tablefmt='fancy_grid'))
            wrapper_printer(fpXn=fpXn, mode='converge')
            condition = False
        elif count == 99:
            wrapper_printer(count=count, mode='indefinite')
            condition = False
            raise InfiniteIteration

        count += 1
        
    return n


def main():
    fx = input('Formula >> ')
    formula = lambda x: eval(fx)
    n = float(input('Xn >> '))

    try:
        start = default_timer()
        try:
            print(f'The root is: {newton_raphson(formula, n):.4f}\n')
            print(f'Computation took {round(default_timer() - start, 3)} ',
                end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
        except InfiniteIteration:
            print('ERROR: InfiniteIteration / IndefiniteFunction\n')
    except ZeroDivisionError as ex:
        print(f'\nThere is a problem. ERROR: {ex}')
    except Exception as ex:
        print(f'\nNon-mathematic problem encountered. ERROR: {ex}')
    finally:
        print('----------------------------------------------------------------\n')


if __name__ == '__main__':
    main()