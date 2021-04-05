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
                       'fc': fc, 'CoS': '-' if fa*fc <= 0 else '+'}
        
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
