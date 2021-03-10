class stu(object):
    __slots__ = ('name', 'page', )

    def __init__(self):
        #如果有下面属性使用，会报错
        #self.noslots ='没有在__slots__中的属性，类中也不可以定义'
        pass

    def __len__(self):
        return 666

    def __str__(self):
        return "这是由__str__()返回的"	

    def __repr__(self):
        return "这是由__repr__()返回的"


s = stu()

print( len(s))
print( s )

