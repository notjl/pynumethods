from timeit import default_timer
from math import *

from tabulate import tabulate
from error_handler import error_printer, InfiniteIteration

headers = ['[I]']
floatformat = [None]


class Formula(object):
    def __init__(self, formula: str, n: float, header: str):
        self.header = header
        self.formula = formula
        self.curr_Xn = n
        self.prev_Xn = 0.0
        self.error = None
        self.flag = True
        self.condition = False

    def f(self):
        x = self.curr_Xn
        if self.flag:
            self.prev_Xn = self.curr_Xn
            self.curr_Xn = eval(self.formula)
            self.e()

    def e(self):
        self.error = round(abs(((self.curr_Xn-self.prev_Xn)/self.curr_Xn)*100), 4)

    def flagger(self):
        x = self.curr_Xn

        if isclose(self.error, 0.0000, rel_tol=1e-4):
            self.mode = '0'
            self.root = self.curr_Xn
            self.condition = True
            self.flag = False
            self.curr_Xn = None
            self.error = None
        elif isclose(self.prev_Xn, self.curr_Xn, abs_tol=1e-4):
            self.mode = 'converge'
            self.root = self.curr_Xn
            self.condition = True
            self.flag = False
            self.curr_Xn = None
            self.error = None

    def wrapper_printer(self):
        if self.mode == '0':
            print(f'Since {self.header} %e is close to 0.0000%, stopping iteration')
        elif self.mode == 'converge':
            print(f'Since {self.header} is converging, stopping iteration')


def fixed_point(formulae: list) -> list:
    data = []
    count = 0
    condition = True

    while condition:
        row = [count]
        formulae_flags = []

        for i in range(len(formulae)):
            row.append(formulae[i].curr_Xn)
            row.append(formulae[i].error)
            formulae[i].f()
            if formulae[i].flag:
                formulae[i].flagger()
            formulae_flags.append(formulae[i].condition)

        data.append(row)

        if all(formulae_flags):
            print('\n')
            print(tabulate(data, headers=headers, floatfmt=floatformat,
                tablefmt='fancy_grid'))
            print('\n')
            for i in range(len(formulae)):
                formulae[i].wrapper_printer()
            condition = False
        elif count >= 99:
            error_printer(count=count)
            condition = False
            raise InfiniteIteration

        count += 1


def main():
    formulae = []
    formula_range = int(input('How many possible iterative formula? '))
    n = float(input('Xn >> '))

    for i in range(formula_range):
        f = input(f'{chr(ord("f")+i)}(x) >> ')
        formulae.append(Formula(formula=f, n=n, header=f'{chr(ord("f")+i)}(x)'))
        headers.extend([f'{chr(ord("f")+i)}(x)', f'{chr(ord("f")+i)}(x) %e'])
        floatformat.extend(['.4f', '.4f'])

    start = default_timer()
    try:
        fixed_point(formulae=formulae)
        print('The roots are: ', end='')

        for i in range(formula_range):
            if formula_range > 1:
                print(end=f'{formulae[i].root:.4f}, ' if formula_range-1 != i else f'{formulae[i].root:.4f}\n\n')

        print(f'Computation took {round(default_timer() - start, 3)} ',
        end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')
    except InfiniteIteration:
        print('ERROR: InfiniteIteration / IndefiniteFunction\n')
    except Exception as ex:
        print(f'\nNon-mathematic problem encountered. ERROR: {ex}')
    finally:
        print('----------------------------------------------------------------\n')


if __name__ == '__main__':
    main()
