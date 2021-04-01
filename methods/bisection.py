from math import isclose
from math import log
from timeit import default_timer

from numba import jit
from tabulate import tabulate

headers = ['[I]', 'a', 'b', 'c', 'f(a)', 'f(c)', '(b-c)', 'swap']
floatformat = (None, '.4f', '.4f', '.4f', '.4f', '.4f', '.4f', None)


def wrapper_printer(b=0, c=0, e=0):
    print(f'\n\nSince {b-c:.4f} <= {e:.4f}, c is the root.')


@jit(forceobj=True)
def bisection(a, b, e, f):
    data = []
    count = 1
    condition = True

    while condition:
        row = [count]
        c = (a + b)/2
        fa = f(a)
        fc = f(c)
        bc = b-c
        row.extend([a, b, c, fa, fc, bc,
            'b = c' if fa * fc <= 0  else 'a = c'])
        data.append(row)

        if bc <= e or round(bc, 4) <= e:
            print(tabulate(data, headers=headers, floatfmt=floatformat,
                tablefmt='fancy_grid'))
            wrapper_printer(b, c, e)
            condition = False

        if fa * fc <= 0:
            b = c
        else:
            a = c
        
        count += 1

    return c


def main():
    fx = input('Formula >> ')
    formula = lambda x: eval(fx)
    a = float(input('a Value >> '))
    b = float(input('b Value >> '))
    epsilon = float(input('Error Tolerance >> '))

    if formula(a) * formula(b) > 0.0:
        print(f'\nf(a) = {formula(a):.4f}, f(b) = {formula(b):.4f}')
        print('f(a) and f(b) should have different signs')
        print('Try again with different values...\n\n')
    else:
        print(f'\nf(a) = {formula(a):.4f}, f(b) = {formula(b):.4f}')
        print('f(a) and f(b) has different signs')

        try:
            print(f'n = {log((b-a)/epsilon)/log(b):.4f}')
            print(f'Expected iteration: {round(log((b-a)/epsilon)/log(b), 1)}\n\n')
        except (ZeroDivisionError, ValueError) as ex:
            print(f'Expected iteration: N/A || Reason: {ex}\n\n')
        except Exception as ex:
            print(f'\nNon-mathematic problem encountered. ERROR: {ex}')

        start = default_timer()
        print(f'The root is: {bisection(a, b, epsilon, formula):.4f}\n')
        print(f'Computation took {round(default_timer() - start, 3)} ',
            end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
            
    print('-----------------------------------------------------------------------------------------------\n')


if __name__ == '__main__':
    main()