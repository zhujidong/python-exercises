# -*- coding: utf_8 -*-

'''
@log
def ppp(arg)
相当于   
ppp = log(ppp) ，则：
ppp(arg) 同 log(ppp)(arg)

@log(sta)
def ppp(arg)
相当于
ppp = log(sta)(ppp)
ppp（arg）同 log(sta)(ppp)(arg)

'''

import functools 

def log(func):
    def wrapper(*args, **kw):
        print('装饰器内层函数执行。默认传入被装饰的的函数对像:', func)
        return func(*args, **kw)
    print('**ppp被定义的作用域中，装修器表达示就被求值，不调用ppp()就会输出此行**\n') 
    return wrapper

@log
def ppp():
    print('ppp函数体被执行。这是ppp本身的输出')

print('下面调用ppp():')
ppp()
print('ppp是指向包装的函数的：ppp.__name__是', ppp.__name__)

print('\n------下面加上 @functools.wraps ------------\n')

def log1(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('装饰器内层函数执行。默认传入被装饰的的函数对像:', func)
        return func(*args, **kw)
    print('**ppp1被定义的作用域中，装修器表达示就被求值，不调用ppp1()就会输出此行**\n') 
    return wrapper

@log1
def ppp1():
    print('ppp1函数体被执行。这是ppp1本身的输出')

print('下面调用ppp1():')
ppp1()
print('ppp1的属性经过@wraps传递给了wrapper函数，所以值与上例不同：ppp1.__name__是', ppp1.__name__)


print('\n------下面是带参装修器 ------------\n')

def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('带参装饰器，这是参数：%s\n这是装饰函数体，被装饰的函数名：%s' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log2('装饰器参数')
def ppp2():
    print('这是被装饰的函数ppp2的函数体')

ppp2()

