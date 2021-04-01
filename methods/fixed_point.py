class Formula:
    def __init__(self, formula, n):
        self.formula = formula
        self.curr_Xn = n
        self.prev_Xn = 0

    def f(self) -> float:
        return eval(self.formula)


def fixed_point(formula_list):
    pass


if __name__ == '__main__':
    formula_list = []
    for i in range(5):
        formula_list.append(Formula(input('Formula >> '), float(input('Xn >> '))))
    for i in range(5):
        print(f'{chr(ord("f") + i)}(x) = {formula_list[i].formula}, Xn = {formula_list[i].curr_Xn}')
