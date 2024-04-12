import time


t = "Tue, 09 Apr 2024 09:34:32 +0900"
_struct = time.strptime(t, "%a, %d %b %Y %H:%M:%S %z")
print(_struct.tm_gmtoff) #带有时区信息
print(time.mktime(_struct))
print(time.strftime("%d %b %Y %H:%M:%S %z",_struct)) #不能显示时区信息

t = "Tue, 09 Apr 2024 09:34:32 +0800"
_struct = time.strptime(t, "%a, %d %b %Y %H:%M:%S %z")
print(_struct.tm_gmtoff)
print(time.mktime(_struct))
print(time.strftime("%d %b %Y %H:%M:%S %z",_struct))

now = time.localtime()
print(now.tm_gmtoff)
print(time.mktime(now))

from os import path

ft = path.getmtime(__file__) #本地时间
print(ft)
print(time.localtime(ft).tm_gmtoff)


l =time.localtime()
print('---------------\n',l)
print(l.tm_gmtoff)
print(l.tm_zone)
