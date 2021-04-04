from math import isclose
from timeit import default_timer

from error_handler import InfiniteIteration, error_printer
from sympy import Symbol, sympify, diff
from sympy.core.function import Function
from sympy.parsing.sympy_parser import implicit_multiplication_application, \
    parse_expr, standard_transformations, convert_xor, function_exponentiation
from tabulate import tabulate

headers = ['[I]', 'Xn', 'f(Xn)', 'f\'(Xn)', '%e']
floatformat = (None, '.4f', '.4f', '.4f', '.4f')

x = Symbol('x')
transformations = standard_transformations + \
    (convert_xor, implicit_multiplication_application, function_exponentiation)


def wrapper_printer(fpXn=0, error=0, mode='default'):
    if mode == 'default':
        print(f'\n\nSince {error:.4f}% = 0.0000%, Xn is the root')
    elif mode == 'converge':
        print(f'\n\nSince {fpXn:.4f} is converging , Xn is the root')


def newton_raphson(f: Function, n: int, table_flag: bool = False, conclude_flag: bool = False) -> float:
    data = []
    count = 0
    prev_n = 0
    fp = diff(f, x)

    while True:
        row = [count]
        fXn = f.subs(x, n)
        fpXn = fp.subs(x, n)
        error = (((n-prev_n)/n)*100)

        row.extend([n, fXn, fpXn, error if count > 0 else None])
        data.append(row)

        prev_n = n
        n = n - (fXn/fpXn)

        if isclose(round(error, 4), 0.0, rel_tol=1e-4):
            if table_flag:
                print(tabulate(data, headers=headers, floatfmt=floatformat,
                               tablefmt='fancy_grid'))
            if conclude_flag:
                wrapper_printer(error=error)
            break
        elif isclose(fpXn, fp.subs(x, n), rel_tol=1e-4):
            if table_flag:
                print(tabulate(data, headers=headers, floatfmt=floatformat,
                               tablefmt='fancy_grid'))
            if conclude_flag:
                wrapper_printer(fpXn=fpXn, mode='converge')
            break
        elif count == 99:
            error_printer(count=count)
            raise InfiniteIteration

        count += 1

    return n


formula = parse_expr(input('Formula >> '), transformations=transformations)
n = float(sympify(input('Xn >> ')))

if input('Tabulate? [y|Default: n] >> ').lower() == 'y':
    table_flag = True
else:
    table_flag = False

if input('Show conclusion [y|Default: n] >> ').lower() == 'y':
    conclude_flag = True
else:
    conclude_flag = False

try:
    start = default_timer()
    print(
        f'The root is: {newton_raphson(f=formula, n=n, table_flag=table_flag, conclude_flag=conclude_flag):.4f}\n')
    print(f'Computation took {round(default_timer() - start, 3)} ',
          end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
except InfiniteIteration:
    print('ERROR: InfiniteIteration / IndefiniteFunction\n')
except ZeroDivisionError as ex:
    print('\nERROR:', ex)
    print('Try with a float number instead of exactly 0')
except Exception as ex:
    print('\nNon-mathematical error encountered. ERROR:', ex)
finally:
    print('-----------------------------------------------------------------------------------------------\n')

if __name__ == '__main__':
    pass
