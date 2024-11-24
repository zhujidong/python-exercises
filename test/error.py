import traceback

def this_fails():
    x = 1/0

try:
    this_fails()
except ZeroDivisionError as exc:
    print('异常实例：' + exc.__str__())
    
    #traceback.print_exception(exc)
    info = traceback.format_exception(exc)
    print( 'traceback：' + ''.join(info))