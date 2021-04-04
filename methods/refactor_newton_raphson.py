from math import isclose
from timeit import default_timer

from .error_handler import InfiniteIteration, error_printer
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


def newton_raphson(f: Function, n: int, tabulate: bool = False,
                   conclude: bool = False, rational: bool = False,
                   main_flag: bool = False) -> float:
    """
    Using Newton-Raphson method, it returns the root.
    - Utilizes the derivative of f(x)
    - is an open method that finds the root x of a function such that f(x)

    ..WARNING:
        - Always use 'x' as a symbol

    Examples
    ========

    ** Non-pythonic expressions will be parsed by SymPy module
    >>> from newton_raphson import newton_raphson
    >>> newton_raphson('x^2-8x+11', 1)
    1.763932022500022

    ** Using pythonic expressions is also accepted
    >>> newton_raphson('x**2-8*x+11', 1)
    1.763932022500022

    ** Turning rational True
    >>> newton_raphson('x^2-8x+11', 1, rational=True)
    3842389/2178309

    Parameters
    ==========
    f :
        - Should be STRING
        - Mathematical expression
        - A mathematical function
        - Example: 
            'x^2-8x+11'
            'x**3-3*x+1'
            'x^3+10x^2-5'

    n :
        - the 'x' value of the function

    tabulate :
        - Tabulates the data, showing the iterated values
        - Defaults to False

    conclude :
        - Prints the conclusion why it stopped iterating
        - Defaults to False

    rational :
        - Returns fraction/rational value
        - Defaults to False

    main_flag :
        - Only used when using the __name__ == '__main__'
        - Remember to change 'from .error_handler' to 'from error_handler'
        - Defaults to False
    """

    if not main_flag:
        f = parse_expr(f, transformations=transformations)
        n = sympify(n)

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
            if tabulate:
                print(tabulate(data, headers=headers, floatfmt=floatformat,
                               tablefmt='fancy_grid'))
            if conclude:
                wrapper_printer(error=error)
            break
        elif isclose(fpXn, fp.subs(x, n), rel_tol=1e-4):
            if tabulate:
                print(tabulate(data, headers=headers, floatfmt=floatformat,
                               tablefmt='fancy_grid'))
            if conclude:
                wrapper_printer(fpXn=fpXn, mode='converge')
            break
        elif count == 99:
            error_printer(count=count)
            print('ERROR: InfiniteIteration / IndefiniteFunction\n')
            raise InfiniteIteration

        count += 1

    return float(n) if not rational else n


def main():
    formula = parse_expr(input('Formula >> '), transformations=transformations)
    n = float(sympify(input('Xn >> ')))

    if input('Tabulate? [y|Default: n] >> ').lower() == 'y':
        tabulate = True
    else:
        tabulate = False

    if input('Show conclusion [y|Default: n] >> ').lower() == 'y':
        conclude = True
    else:
        conclude = False

    start = default_timer()
    print(
        f'The root is: {newton_raphson(f=formula, n=n, tabulate=tabulate, conclude=conclude, main_flag=True, rational=True): .4f}\n')
    print(f'Computation took {round(default_timer() - start, 3)} ',
          end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
    print('-----------------------------------------------------------------------------------------------\n')


if __name__ == '__main__':
    main()
