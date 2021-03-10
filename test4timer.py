from threading import Timer
import time
import datetime

s=None
n=None
c=0

def MonitorSystem(logfile = None):
    global s
    global c
    
    c=c+1
    if c % 2 ==0:
        t = 2
    else:
        t = 5
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{t}秒间隔 sysinfo：{ts}'
    print(line)

    #启动定时器任务，每三秒执行一次
    s=Timer( t, MonitorSystem)
    s.start()

def MonitorNetWork(logfile = None):
    global n
    t = 1    
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    line = f'{t}秒间隔 network：{ts}'
    print(line)
   
   #启动定时器任务，每秒执行一次
    n=Timer( t, MonitorNetWork)
    n.start()

MonitorSystem()
MonitorNetWork()

while True:
    str = input()
    if str=='q':
        s.cancel()
        n.cancel()
        break
    if str=='s':
        s.cancel()
    if str=='n':
        n.cancel()
    print ("你输入的内容是: ", str)
    