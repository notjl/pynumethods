from math import isclose
from typing import Tuple, Union

from sympy import Symbol, diff, sympify
from sympy.core.function import Function
from sympy.parsing.sympy_parser import (convert_xor, function_exponentiation,
                                        implicit_multiplication_application,
                                        parse_expr, standard_transformations)

from .error_handler import InfiniteIteration

x = Symbol('x')
transformations = standard_transformations + \
    (convert_xor, implicit_multiplication_application, function_exponentiation)


# def wrapper_printer(fpXn=0, error=0, mode='default'):
#     if mode == 'default':
#         print(f'\n\nSince {error:.4f}% = 0.0000%, Xn is the root')
#     elif mode == 'converge':
#         print(f'\n\nSince {fpXn:.4f} is converging , Xn is the root')


def newton_raphson(f: Function, n: float, rational: bool = False,
                   iterated_data: bool = False) -> Union[float, Tuple[float, list]]:
    """
    Using Newton-Raphson method, returns float (or tupled with iterated data).
    - Utilizes the derivative of f(x)
    - is an open method that finds the root x of a function such that f(x)

    ..Note:
        - Return iterated_data defaults to False
        - Always use 'x' as a symbol

    Algorithm
    =========
    1. Solve f(x), f'(x), error %
    2. n = n - (f(x)/f'(x))
    3. if error % is converging to 0, return n as root
    4. if previous f'(x) is converging to next f'(x), return n as root

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

    Exceptions
    ==========
    InfiniteIteration :
        - Raised when the function passed is indefinite and
        iteration reaches 99, assuming it is indefinite.

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

    rational :
        - Returns fraction/rational value
        - Defaults to False

    iterated_data:
        - Returns the iterated data in dictionary
    """
    f = parse_expr(f, transformations=transformations)
    n = sympify(n)

    data = {}
    count = 0
    prev_n = 0
    fp = diff(f, x)

    while True:
        fXn = f.subs(x, n)
        fpXn = fp.subs(x, n)
        error = (((n-prev_n)/n)*100)

        data[count] = {'Xn': n, 'fx': fXn, 'fpx': fpXn,
                       'e%': error if count > 0 else None}

        prev_n = n
        n = n - (fXn/fpXn)

        if isclose(round(error, 4), 0.0, rel_tol=1e-4):
            break
        elif isclose(fpXn, fp.subs(x, n), rel_tol=1e-4):
            break
        elif count == 99:
            raise InfiniteIteration

        count += 1

    if not rational:
        n = float(n)

    if iterated_data:
        return n, data
    else:
        return n
