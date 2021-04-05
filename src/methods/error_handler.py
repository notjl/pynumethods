class SameSigns(Exception):
    '''Raised when values of f(a) and f(b) has the same sign'''
    def __init__(self, message='f(a) and f(b) values has the same sign') -> None:
        self.message = message
        super().__init__(self.message)


class InfiniteIteration(Exception):
    '''Raised when the iteration reaches 99 or greater'''
    def __init__(self, message='Iteration reached 99, it is assumed the passed function is indefinite') -> None:
        self.message = message
        super().__init__(self.message)