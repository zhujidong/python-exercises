# -*- coding: utf_8 -*-

#对像的逻辑值测试

class duixiang( object ):
    def __init__(self):  
        print('这是一个对像，默认逻辑值为：True')
    
    def __bool__(self):
       return False
    
    def __len__(self):
        return 1
        
a=duixiang()

if a:
    print('对像默认逻辑值为 True')
else:
    print('但若对像的bool()方法返回False或len()方法返回0，对像的值为False')
    print('如果同时有bool()和len()方法，当然是以bool()方法的值为准')