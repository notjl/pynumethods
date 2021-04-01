from math import *

from tabulate import tabulate

headers = ['[I]']
floatformat = [None]


class Formula:
    def __init__(self, formula: str, n: float):
        self.formula = formula
        self.curr_Xn = n
        self.prev_Xn = 0.0
        self.error = self.e()
        self.flag = True

    def f(self):
        x = self.curr_Xn
        self.prev_Xn = self.curr_Xn
        self.curr_Xn = eval(self.formula)
        self.e()

    def e(self):
        self.error = round(abs(((self.curr_Xn-self.prev_Xn)/self.curr_Xn)*100), 4)


def fixed_point(formulae: list) -> list:
    data = []
    count = 0
    condition = True

    while condition:
        row = [count]

        for i in range(len(formulae)):
            row.append(formulae[i].curr_Xn)
            row.append(formulae[i].error)
            formulae[i].f()
            
        data.append(row)

        if count == 5:
            print(tabulate(data, headers=headers, floatfmt=floatformat))
            condition = False

        count += 1


if __name__ == '__main__':
    formulae = []
    formula_range = int(input('How many possible iterative formula? '))
    n = float(input('Xn >> '))

    for i in range(formula_range):
        f = input(f'{chr(ord("f")+i)}(x) >> ')
        formulae.append(Formula(formula=f, n=n))
        headers.extend([f'{chr(ord("f")+i)}(x)', f'{chr(ord("f")+i)}(x) %e'])
        floatformat.extend(['.4f', '.4f'])

    fixed_point(formulae=formulae)
