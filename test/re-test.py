import re

a = re.match( '[gdpi]( +\d+)+$', 'd         353663  453   44')
print(a.group())
print(a.groups())

tmp = re.sub( ' +', ' ', a.group() )
print( tmp )
print( tmp.split(' ') )