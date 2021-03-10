import inspect

def decorator(f):
    f.add_des = '类的方法也能添加属性，函数也是对像'
    return f

class a_class(object):
    gol = 100

    @decorator
    def class_fun(self):
        print('成员方法')

#得到类中的可调用成员
for name,val in inspect.getmembers(a_class, callable):
    print( name,val )
    #这个成员有一个 “add_des"的属性
    if hasattr( val, 'add_des'):
        print( name, val, 'add_des')
        break

#这个类的成员函数多了一个属性。
print( a_class.class_fun.add_des)