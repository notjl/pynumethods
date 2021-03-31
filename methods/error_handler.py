class Error(Exception):
    '''Base class for custom errors'''
    pass

class InfiniteIteration(Error):
    '''Raised when the iteration reaches 99 or greater'''
    pass