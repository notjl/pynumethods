from math import isclose
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


def false_position(f: Function, a: float, b: float, rational: bool = False,
                   iterated_data: bool = False) -> Union[float, Tuple[float, dict]]:
    """
    Using false-position method, returns root (or tupled with iterated data)
    - The same as bisection method, because the size of an interval
    containing a root is reduced through iteration.

    ..Note:
        - Return iterated_data defaults to False
        - Always use 'x' as symbol

    Algorithm
    =========
    1. Find two numbers (a, b) of which f(x) has different signs
    2. Define c = (a*fb-b*fa)/(fb-fa)
    3. if b and c are converging, return c as root
    4. if f(a)f(c) <= 0, b = c else a = c

    Examples
    ========
    ** Non-pythonic expressions will be parsed by SymPy module
    >>> false_position('x^2-8x+11', 1, 2)
    1.7639484978540771

    ** Using pythonic expressions is also accepted
    >>> false_position('x**2-8*x+11', 1, 2)
    1.7639484978540771

    ** Turning rational True
    >>> false_position('x^3-3x+1', 0, 1, rational=True)
    119624146949151814554649/344443180703677909347131
    
    ** Turning iterated_data True
    >>> false_position('x^3-3x+1', 0, 1, iterated_data=True)
    (0.3472971847047936, {1: {'a': 0, 'b': 1, 'fa': 1, 'fb': -1, 'c': 1/2, 'fc': -3/8, 'CoS': '-'}, ...)

    Iterated data
    =============
    count / iteration :
        - The first key you see in the dictionary

    a :
        - Value of the first interval

    b :
        - Value of the second interval

    fa :
        - Value of the f(a)

    fb :
        - Value of the f(b)

    c :
        - Value of (a*fb-b*fa)/(fb-fa) [value of the root]

    fc :
        - Value of the f(c)

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

    rational :
        - Returns fraction/rational value
        - Defaults to False

    iterated_data:
        - Returns the iterated data in dictionary
        - Defaults to False
    """

    f = parse_expr(f, transformations=transformations)
    a = sympify(a)
    b = sympify(b)

    if f.subs(x, a) * f.subs(x, b) > 0.0:
        raise SameSigns

    data = {}
    count = 1

    while True:
        fa = f.subs(x, a)
        fb = f.subs(x, b)
        c = (a*fb-b*fa)/(fb-fa)
        fc = f.subs(x, c)

        data[count] = {'a': a, 'b': b, 'fa': fa, 'fb': fb, 'c': c,
                       'fc': fc}
        
        if isclose(b, c, rel_tol=1e-4):
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
