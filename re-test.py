import re

a = re.match( 'l|[gdi]( +\d+)+$', 'd   56 44')
print(a.group())
print(a.groups())