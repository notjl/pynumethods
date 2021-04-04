from math import log
from timeit import default_timer
from typing import Tuple

from sympy import Symbol, sympify
from sympy.core.function import Function
from sympy.parsing.sympy_parser import implicit_multiplication_application, \
    parse_expr, standard_transformations, convert_xor, function_exponentiation
from tabulate import tabulate

x = Symbol('x')
transformations = standard_transformations + \
    (convert_xor, implicit_multiplication_application, function_exponentiation)


def bisection(f: Function, a: float, b: float, error: float) -> Tuple[float, dict]:
    count = 1

    while True:
        c = (a + b) / 2
        fa = f.subs(x, a)
        fc = f.subs(x, c)
        bc = b-c

        if bc <= error or round(bc, 4) <= error:
            break

        if fa*fc <= 0:
            b = c
        else:
            a = c
        
        count +=1

    return c


def main():
    formula = parse_expr(input('Formula >> '), transformations=transformations)
    a = float(sympify(input('a Value >> ')))
    b = float(sympify(input('b Value >> ')))
    epsilon = float(sympify(input('Error Tolerance >> ')))

    root = bisection(f=formula, a=a, b=b, error=epsilon)


if __name__ == '__main__':
    main()