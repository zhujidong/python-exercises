def abs(n):
    '''
    Function to get absolute value of number.
    
    Example:
    
    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    >>> abs('a')
    Traceback (most recent call last):
        ...
    TypeError: '>=' not supported between instances of 'str' and 'int'
    '''
    return n if n >= 0 else (-n)


if __name__=='__main__':
    import doctest
    doctest.testmod()