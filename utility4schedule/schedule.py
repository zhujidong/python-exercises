# -*- coding:utf_8 -*-

import time
from threading import Timer


class Schedule(object):
    '''
    任务调度，以线程方式运行。支持按周循环，周中每天可定义不同的时间
    注册为线程的对像或方法，只能以元组的形式接受位置参数
    
    '''

    def __init__(self) -> None:

        self.threads = {}
        '''
        记录所有线程的信息，key为“线程名”，value为线程信息。
        value仍是一个字典，各key记录的值含义如下：
            fun:str,要注册为线程的函数或方法
            param:tuple,线程的参数，只能以元组的形式传递位置参数给fun ****
            schedule:str,线程执行的时间计划
            retry:tuple(int,int)，线程执行失败时，重复执行次数与时间间隔（默认6分种）
            errors:int,记录线程执行失败次数
            handle:线程的句柄
        '''


    def reg_thread(self, name:str, fun:object, param:tuple, schedule:str, retry:tuple=(1,360),at_once:bool=False) -> None:
        '''
        将函数或方法注册为线程，并启动线程。
        *要求注册的线程成功返为True,失败返回False

        :param:
            name:str,线程注册的名称
            at_once:bool,注册线程后是否立即执行一次
            其它参数为此线程相关信息，含义见__init__()中 threads 定义
        '''
        thread = {'fun':fun, 'param':param, 'schedule':schedule, 'retry':retry, 'errors':0, 'handle':None}
        self.threads[name] = thread
        if at_once:
            #立即执行，则不传递first_time参数，默认为假，首次也会执行线程
            self._run_thread(name)
        else:
            self._run_thread(name, True)
        return None


    def _run_thread(self, name, first_time=False) -> None:
        '''
        调用Timer启动线程

        :param:
            name:str,线程注册的名称
            first_time:bool,是否第一次执行，第一次只是按计划启动线程，并不执行
        '''
        if first_time:
            interval, nextdatetime = Schedule.get_interval(self.threads[name]['schedule'])
            nextdatetime = time.strftime("%m月%d日%H:%M", nextdatetime)
            info = F'“{name}”线程注册完成，按计划将于{nextdatetime}首次启动'
        else:
            now = time.strftime("%m月%d日%H:%M", time.localtime(time.time()))
            print(F'\r\n----------------------------\r\n{now}：”{name}“线程启动...')
            
            #调用注册的线程函数
            rs = self.threads[name]['fun'](*self.threads[name]['param'])
                                        #将元组展开成各个参数
            #生成下次的执行间隔，比较准
            interval, nextdatetime = Schedule.get_interval(self.threads[name]['schedule'])
            nextdatetime = time.strftime("%m月%d日%H:%M", nextdatetime)
            if rs:
                self.threads[name]['errors'] = 0
                info = F'“{name}”线程执行完毕，下次计划于{nextdatetime}启动'
            else:
                self.threads[name]['errors'] += 1
                if self.threads[name]['errors']  <= self.threads[name]['retry'][0]:
                    interval = self.threads[name]['retry'][1]
                    info = F'”{name}“线程执行失败，将在{interval/60}分种后重启...'
                else:
                    info = F'”{name}“线程已失败{self.threads[name]["errors"]}次，不再重试，将在下次计划时间（{nextdatetime}）启动。'
                    self.threads[name]['errors'] = 0
        print(info,'\r\n----------------------------\r\n')
        self.threads[name]['handle'] = Timer(interval, self._run_thread, args=(name,))
        self.threads[name]['handle'].start()
        return None


    def close_threads(self) -> None:
        for thread in self.threads.values():
            if thread['handle']:
                thread['handle'].cancel()
        return None


    @staticmethod
    def get_interval(schedule:list[tuple]) -> tuple:
        """
        根据配置文件中计划，计算到下次计划的间隔秒数。
        可实现按周循环，周内每天可指定不同的任务时间（可指定时间或间隔），配置文件中的形式如下：
            [schedule]
            6 , 7 = 08: 00, 12:00, 17:00, 20:00 # 表示周六日在此四个时间执行。（需从小到大排序）
            4,2, 6 = 600, 08:00, 20:00 #表示周一三五在8-20点之间，每600秒执行一次
        * 星期若重复，则后面的会覆盖前面的设置
            
        :param:
            schedule,执行计划的的时间，从配置文件中读入后是一个元组的列表。如上例，则是：
                [   ('6 , 7', '08: 00, 12:00, 17:00, 20:00'),
                    ('1,3,5', '600, 08:00, 20:00')    ]
        :return: 
            至下次计划的间隔秒数, 下次计划的日期时间
        """
        
        #整理成按星期排序的计划列表
        temp ={}
        for sche in schedule:
            #转换成以星期几为键的字典，以消除重复的计划
            week = sche[0].replace(' ', '').split(',')
            table = sche[1].replace(' ', '').split(',')
            for w in week:
                temp[int(w)] = table
        schedule = sorted(temp.items(),key=lambda x:x[0])

        #当前时间戳，星期几，日期，时间
        stamp = time.time()
        struct = time.localtime(stamp)
        day_of_week = struct[6] + 1 # 1,周一；7，周日        
        date_ = time.strftime("%Y-%m-%d", struct)
        time_ = time.strftime("%H:%M", struct)

        #提取当天的计划列表 和 下个天的星期几和对应计划列表
        table = None
        for sche in schedule:
            if sche[0] == day_of_week:
                table = sche[1]
            elif sche[0] > day_of_week:
                next_day_of_week = sche[0]
                next_table = sche[1]
                break
        else:
            #只有被break，才“不会”执行此处。（一次没执行或顺利执行完循环，都“会”执行此处）
            #没有被break，说明在列表中没有找到“next”的数据 ，则设置为第一个。
            next_day_of_week = schedule[0][0]
            next_table = schedule[0][1]
        
        #先在当天中查找下次计划，找到设置 next_stamp，否则置为 None
        next_stamp = None
        if table and ':' in table[0]:
            #当天有计划，并且是 定点执行的
            for tb in table:
                if tb > time_:
                    next_stamp = time.mktime(time.strptime(F'{date_} {tb}', '%Y-%m-%d %H:%M'))  
                    break
        elif table:
            #当天有计划，按时间间隔执行
            next_stamp = stamp + int(table[0])
            next_time = time.strftime("%H:%M", time.localtime(next_stamp))
            if next_time <=  table[1]:
                #没到当天计划开始时间
                next_stamp = time.mktime(time.strptime(F'{date_} {table[1]}', '%Y-%m-%d %H:%M'))  
            elif next_time >= table[2]:
                #不是今天的计划了
                next_stamp =None

        #当天没有计划或当天计划的时间之外,设置为下次那天的开始时间就可
        if next_stamp is None:
            if ':' in next_table[0]:
                next_time = next_table[0]
            else:
                next_time = next_table[1]

            #下次与今天相距的天数
            if next_day_of_week <= day_of_week:
                next_day_of_week += 7
            days = next_day_of_week - day_of_week

            # ***用今日、下次时间 生成的时间戳，还需要加上差的天数***
            next_stamp = time.mktime(time.strptime(F'{date_} {next_time}', '%Y-%m-%d %H:%M'))  
            next_stamp += days*24*3600

        interval = next_stamp - stamp
        return interval, time.localtime(next_stamp)