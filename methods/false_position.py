from math import isclose
from timeit import default_timer

from numba import jit


def wrapper_printer(count=0, a=0, b=0, fa=0, fb=0, c=0, fc=0, mode='default'):
    if mode == 'default':
        print(f'I[{count:2}]: a = {a:.4f}, b = {b:.4f}, f(a) = {fa:.4f},',
            f' f(b) = {fb:.4f}, c = {c:.4f}, f(c) = {fc:.4f}, CoS: ',
            end="-\n" if fa * fc <= 0 else "+\n")
    elif mode == 'converge':
        print(f'\n\nSince {b:.4f} is converging with {c:.4f}, c is the root')


@jit(forceobj=True)
def false_position(a, b, f):
    count = 1
    condition = True

    print('ITERATION:')
    while condition:
        c = (a*f(b) - b*f(a))/(f(b)-f(a))

        wrapper_printer(count, a, b, f(a), f(b), c, f(c))

        if isclose(b, c, rel_tol=1e-4):
            wrapper_printer(b=b, c=c, mode='converge')
            condition = False

        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
        
        count += 1
        
    return c


if __name__ == '__main__':
    while 1:
        fx = input('Formula >> ')

        if fx.lower() == 'exit':
            print('Exiting...')
            break

        formula = lambda x: eval(fx)
        a = float(input('a Value >> '))
        b = float(input('b Value >> '))

        if formula(a) * formula(b) > 0.0:
            print(f'\nf(a) = {formula(a):.4f}, f(b) = {formula(b):.4f}')
            print('f(a) and f(b) should have different signs')
            print('Try again with different values...\n\n')
        else:
            print(f'\nf(a) = {formula(a):.4f}, f(b) = {formula(b):.4f}')
            print('f(a) and f(b) has different signs\n\n')

            start = default_timer()
            print(f'The root is: {false_position(a=a, b=b, f=formula):.4f}\n')
            print(f'Computation took {round(default_timer() - start, 3)} ',
                end='seconds\n' if round(default_timer() - start, 3) > 1.0 else 'ms\n')

        print('-----------------------------------------------------------------------------------------------\n')