class Error(Exception):
    '''Base class for custom errors'''
    pass

class InfiniteIteration(Error):
    '''Raised when the iteration reaches 99 or greater'''
    pass

def error_printer(mode='default', count=0):
    if mode == 'default':
        print(f'\n\nSince I[{count}] >= 99, it is assumed it as an indefinite function.')
        print('Resulting in no definite or approximite root.')
        print('Re-check the function if it is correct.\n')