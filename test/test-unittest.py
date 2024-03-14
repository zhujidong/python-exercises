import unittest

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
#end of abs()

class TestABS(unittest.TestCase):

    def setUp(self):
        print('setUp方法在每个测试开前运行')

    def tearDown(self):
        print('tearDown方法在每个测试后运行')
    #若 setUp() 成功运行，无论测试方法是否成功，都会运行 tearDown() 。

    def test_nomal(self):
        self.assertEqual(abs(1), 1)
        self.assertEqual(abs(0), 0)
        self.assertEqual(abs(-1), 1)

    def test_raise(self):
        with self.assertRaises(TypeError):
            abs('a')

if __name__ == '__main__':
    unittest.main()
