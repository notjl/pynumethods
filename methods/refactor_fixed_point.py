from math import isclose
from typing import Tuple, Union

from sympy import Symbol, sympify
from sympy.core.function import Function
from sympy.parsing.sympy_parser import (convert_xor, function_exponentiation,
                                        implicit_multiplication_application,
                                        parse_expr, standard_transformations)

from .error_handler import InfiniteIteration

x = Symbol('x')
transformations = standard_transformations + \
    (convert_xor, implicit_multiplication_application, function_exponentiation)


def fixed_point(f: Function, n: float, rational: bool = False,
                iterated_data: bool = False) -> Union[float, Tuple[float, list]]:
    """
    Using Fixed-Point method, returns float (or tupled with iterated data).
    - Known as the method of successive submission.

    ..Note:
        - Return iterated_data defaults to False
        - Always use 'x' as a symbol
        - Originally was to take list of formulae. Modularising thos method
        means the need to opt it out.

    ..Usage:
        * Find all the possible iterative formula of f(x),
        Transform them to x = f(x)
            Example:
                f(x) = x^2-8x+11 can be transformed to:
                    x = (x^2+11)/8;
                    x = sqrt(8x-11)
                    x = (8x-11)/x

    Algorithm
    =========
    1. Solve for the new value of n [f(n)] 
    2. If error % is converging to 0, return n as root
    3. if previous n is converging with current n, return n as root

    Examples
    ========
    ** Non-pythonic expressions will be parsed by SymPy module
    >>> fixed_point('(x^2+11)/8', 3)
    1.7639910281905442

    ** Using pythonic expressions is also accepted
    >>> fixed_point('(x**2+11)/8', 3)
    1.7639910281905442

    ** Turning rational True
    >>> fixed_point('(8x-11)/x', 3, rational=True)
    153301943/24583261

    ** Turning iterated_data True
    >>> fixed_point('(8x-11)/x', 3, iterated_data=True)
    (6.236029589402317, {0: {'Xn': 3, 'e%': None}, ...)

    Iterated data
    =============
    count / iteration :
        - The first key you see in the dictionary

    Xn :
        - Value of the iterated approximate root

    e% :
        - Percent error, how accurate the approximate root

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
        - Defaults to False
    """

    f = parse_expr(f, transformations=transformations)
    n = sympify(n)

    data = {}
    count = 0
    prev_n = 0

    while True:
        error = (((n-prev_n)/n)*100)
        data[count] = {'Xn': n, 'e%': error if count > 0 else None}

        prev_n = n
        n = f.subs(x, n)

        if isclose(error, 0.0000, rel_tol=1e-4):
            break
        elif isclose(prev_n, n, abs_tol=1e-4):
            break
        elif count >= 99:
            raise InfiniteIteration

        count += 1

    if not rational:
        n = float(n)

    if iterated_data:
        return n, data
    else:
        return n
