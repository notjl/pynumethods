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

    return c, data


def main():
    formula = parse_expr(input('Formula >> '), transformations=transformations)
    a = float(sympify(input('a Value >> ')))
    b = float(sympify(input('b Value >> ')))
    epsilon = float(sympify(input('Error Tolerance >> ')))

    # root, data = bisection(f=formula, a=a, b=b, error=epsilon)
    # data_to_list: list = []
    # for data_key, data_value in data.items():
    #     row: list = [data_key]
    #     temp: list = []
    #     for value_data_key, value_data_value in data_value.items():
    #         temp.append(value_data_value)
    #     row.extend(temp)
    #     data_to_list.append(row)

    # headers = ['[I]', 'a', 'b', 'c', 'f(a)', 'f(c)', '(b-c)', 'swap']
    # floatformat = (None, '.4f', '.4f', '.4f', '.4f', '.4f', '.4f', None)
    # print(tabulate(data_to_list, headers=headers, floatfmt=floatformat))


if __name__ == '__main__':
    main()
