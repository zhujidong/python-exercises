# -*- coding: utf_8 -*-


def log(func):
    def wrapper(*args, **kw):
        print('装饰器内层函数体输出，被装饰函数名：', func.__name__ )
        return func(*args, **kw)
    print('ppp被定义的作用域中，装修器表达示就被求值，所以不需调用ppp()就会输出此行。\r\n') 
    return wrapper

@log
def ppp():
    print('\r\n*被装饰的函数体输出 ppp')

ppp()



def log1(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('\r\n%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log1('带参装饰')
def now():
    print('2021')

now()
print( now.__name__)

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