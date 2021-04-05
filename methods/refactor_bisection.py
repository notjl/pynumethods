from typing import Tuple, Union

from sympy import Symbol, sympify
from sympy.core.function import Function
from sympy.parsing.sympy_parser import (convert_xor, function_exponentiation,
                                        implicit_multiplication_application,
                                        parse_expr, standard_transformations)

from .error_handler import SameSigns

x = Symbol('x')
transformations = standard_transformations + \
    (convert_xor, implicit_multiplication_application, function_exponentiation)


def bisection(f: Function, a: float, b: float, error: float,
              rational: bool = False, iterated_data: bool = False) -> Union[float, Tuple[float, dict]]:
    """
    Using bisection method, returns root (or tupled with iterated data).
    - Repeatedly bisects an interval and then selects a 
    sub-interval in which a root must lie for further 
    processing.

    ..Note:
        - Return iterated_data defaults to False
        - Always use 'x' as symbol

    Algorithm
    =========
    1. Find two numbers (a, b) of which f(x) has different signs
    2. Define c = (a+b)/2
    3. if (b-c) <= error tolerance, accept c as the root,
        stop iteration
    4. if f(a)f(c) <= 0, b = c else a = c

    Examples
    ========
    ** Non-pythonic expressions will be parsed by SymPy module
    >>> from newton_raphson import newton_raphson
    >>> bisection('x^2-8x+11', 1, 2, 0.001)
    1.7646484375

    ** Using pythonic expressions is also accepted
    >>> bisection('x**2-8*x+11', 1, 2, 0.001)
    1.7646484375

    ** Turning rational True
    >>> bisection('x^3-3x+1', 0, 1, 0.001, rational=True)
    355/1024

    ** Turning iterated_data True
    >>> bisection('x^3-3x+1', 0, 1, 0.001, iterated_data=True)
    (0.3466796875, {1: {'a': 0, 'b': 1, 'c': 1/2, 'fa': 1, 'fc': -3/8, 'bc': 1/2, 'swap': 'b = c'}, ...)

    Iterated data
    =============
    count / iteration :
        - The first key you see in the dictionary

    a :
        - Value of the first interval

    b :
        - Value of the second interval

    c :
        - Value of (a + b)/2 [value of the root]

    fa :
        - Value of the f(a)

    fc :
        - Value of the f(c)
    
    bc :
        - Value of (b - c)

    swap :
        - What values swapped

    Exceptions
    ==========
    SameSign :
        - Raised when values of f(a) and f(b) has the same sign

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

    a :
        - The first interval

    b :
        - The second interval

    error :
        - Error tolerance

    rational :
        - Returns fraction/rational value
        - Defaults to False

    iterated_data:
        - Returns the iterated data in dictionary
    """

    f = parse_expr(f, transformations=transformations)
    a = sympify(a)
    b = sympify(b)
    error = sympify(error)

    if f.subs(x, a) * f.subs(x, b) > 0.0:
        raise SameSigns

    data = {}
    count = 1

    while True:
        c = (a + b) / 2
        fa = f.subs(x, a)
        fc = f.subs(x, c)
        bc = b-c

        data[count] = {'a': a, 'b': b, 'c': c, 'fa': fa, 'fc': fc, 'bc': bc,
                       'swap': 'b = c' if fa * fc <= 0 else 'a = c'}

        if bc <= error or round(bc, 4) <= error:
            break

        if fa*fc <= 0:
            b = c
        else:
            a = c

        count += 1

    if not rational:
        c = float(c)

    if iterated_data:
        return c, data
    else:
        return c
