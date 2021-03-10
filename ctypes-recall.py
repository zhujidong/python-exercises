# -*- coding: utf_8 -*-

from ctypes.wintypes import BOOL, HWND, LPARAM
from ctypes import windll, WINFUNCTYPE, create_string_buffer

#定义回调函数 
@WINFUNCTYPE(BOOL, HWND, LPARAM) 
def print_title(hwnd,extra): 
        title = create_string_buffer(1024) #根据句柄获得窗口标题 
        windll.user32.GetWindowTextA(hwnd,title,255) 
        title = title.value 
        if title:  
                print( title.decode('gbk') ) 
        return 1 

#枚举窗口 
windll.user32.EnumWindows(print_title,0)