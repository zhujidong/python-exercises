# -*- coding:utf_8 -*-

import os
def acc(*args):
	print(*args)
	print( os.path.join('abc',*args))
acc('asfdsf', '000')



