class Formula:
    def __init__(self, formula: str, n: float):
        self.formula = formula
        self.curr_Xn = n
        self.prev_Xn = 0

    def f(self) -> float:
        return eval(self.formula)


def fixed_point(formulae: list) -> list:
    pass


if __name__ == '__main__':
    formulae = []
    formula_range = int(input('How many possible iterative formula? '))
    n = float(input('Xn >> '))

    for i in range(formula_range):
        f = input(f'{chr(ord("f")+i)}(x) >> ')
        formulae.append(Formula(formula=f, n=n))

    for i in range(formula_range):
        print(f'{chr(ord("f")+i)}(x) = {formulae[i].formula}, Xn = {formulae[i].curr_Xn}')
