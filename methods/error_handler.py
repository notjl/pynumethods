class Error(Exception):
    '''Base class for custom errors'''
    pass


class SameSigns(Exception):
    '''Raised when values of f(a) and f(b) has the same sign'''
    def __init__(self, message='f(a) and f(b) values has the same sign') -> None:
        self.message = message
        super().__init__(self.message)


class InfiniteIteration(Error):
    '''Raised when the iteration reaches 99 or greater'''
    pass

def error_printer(mode='default', count=99):
    if mode == 'default':
        print(f'\n\nSince I[{count}] >= 99, it is assumed it as an indefinite function.')
        print('Resulting in no definite or approximite root.')
        print('Re-check the function if it is correct.\n')