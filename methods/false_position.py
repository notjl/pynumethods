from math import isclose
from timeit import default_timer

from tabulate import tabulate

headers = ['[I]', 'a', 'b', 'f(a)', 'f(b)', 'c', 'f(c)', 'CoS']
floatformat = (None, '.4f', '.4f', '.4f', '.4f', '.4f', '.4f', None)


def wrapper_printer(b=0, c=0):
    print(f'\n\nSince {b:.4f} is converging with {c:.4f}, c is the root')


def false_position(a, b, f):
    data = []
    count = 1
    condition = True

    while condition:
        row = [count]
        fa = f(a)
        fb = f(b)
        c = (a*fb - b*fa)/(fb-fa)
        fc = f(c)
        row.extend([a, b, fa, fb, c, fc, '-' if fa * fc <= 0 else '+'])
        data.append(row)

        if isclose(b, c, rel_tol=1e-4):
            print(tabulate(data, headers=headers, floatfmt=floatformat,
                           tablefmt='fancy_grid'))
            wrapper_printer(b=b, c=c)
            condition = False

        if fa * fc <= 0:
            b = c
        else:
            a = c

        count += 1

    return c


def main():
    fx = input('Formula >> ')
    def formula(x): return eval(fx)
    a = float(input('a Value >> '))
    b = float(input('b Value >> '))

    if formula(a) * formula(b) > 0.0:
        print(f'\nf(a) = {formula(a):.4f}, f(b) = {formula(b):.4f}')
        print('f(a) and f(b) should have different signs')
        print('Try again with different values...\n\n')
    else:
        print(f'\nf(a) = {formula(a):.4f}, f(b) = {formula(b):.4f}')
        print('f(a) and f(b) has different signs\n\n')

        start = default_timer()
        try:
            print(f'The root is: {false_position(a=a, b=b, f=formula):.4f}\n')
            print(f'Computation took {round(default_timer() - start, 3)} ',
                  end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
        except Exception as ex:
            print(f'\nNon-mathematic problem encountered. ERROR: {ex}')
        finally:
            print('-----------------------------------------------------------------------------------------------\n')


if __name__ == '__main__':
    main()
