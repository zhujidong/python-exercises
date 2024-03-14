class stu(object):

    def __init__(self):
        self.age = 8
    
        index = 0
        for field in ['aa','bb','cc']:
            self.__setattr__(field, index)
            index += 1

    def __getattr__(self,key):
        print('in getatti')
        return "你访问的属性不存在"

s = stu()

print(s.age)
print(s.name)
input()

print(s.aa)
print(s.cc)