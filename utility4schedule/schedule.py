# -*- coding:utf_8 -*-

import time
from threading import Timer


class Schedule(object):
    '''
    管理计划任务；每个任务以线程方式运行。
    *注册的任务函数，只能以元组的形式接受位置参数*
    '''

    def __init__(self) -> None:

        self.threads = {}
        '''
        记录所有计划任务线程的信息，key为给任务起的“名字”，value为线程信息。
        value仍是一个字典，其key值含义如下：
            fun:str,要注册的任务线程的方法函数
            param:tuple,任务线程的参数，**只能以元组的形式传递位置参数给fun **
            schedule:str,任务执行的计划，计划的定义方式见get_interval()方法
            retry:tuple(int,int)，线程执行失败时，重试次数与时间间隔（默认重试1次，隔360秒后重试）
            errors:int,记录线程执行失败次数
            handle:线程的句柄，供取消等使用
        '''


    def reg_thread(self, name:str, fun:object, param:tuple, schedule:str, retry:tuple=(1,360),at_once:bool=False) -> None:
        '''
        注册一个计划任务， *要求补注册的任凭执行成功返为True,失败返回False

        :param:
            name:str,计划任务的名称
            at_once:bool,注册计划任务后是否立即执行一次，再按按计划执行
            其它参数相关信息，见__init__()。
        '''
        thread = {'fun':fun, 'param':param, 'schedule':schedule, 'retry':retry, 'errors':0, 'handle':None}
        self.threads[name] = thread
        self._run_thread(name, at_once)
        return None


    def _run_thread(self, name, run=True) -> None:
        '''
        调用Timer启动线程，每个线程就是一个等待下次计划时间运行的任务

        :param:
            name:str,要执行的任务名称
            run:bool,为真时，立即执行不管计划，然后设置计划执行
                     为假时，读取计划，设置计划时间执行
                     *当注册线程按计划调用自身时，需为真，因为到了计划时间才调用的，否则永远不能执行计划任务
        '''
        if run:
            now = time.strftime("%m月%d日%H:%M", time.localtime(time.time()))
            print(F'\r\n----------------------------\r\n{now}：”{name}“任务启动...')
            
            #执行计划的任务，成功返回真。       ***此处只将元组展开成位置参数给要执行的方法
            rs = self.threads[name]['fun'](*self.threads[name]['param'])
                                        
            #生成下次的执行间隔
            interval, nextdatetime = Schedule.get_interval(self.threads[name]['schedule'])
            nextdatetime = time.strftime("%m月%d日%H:%M", nextdatetime)
            if rs:
                self.threads[name]['errors'] = 0
                info = F'“{name}”任务执行完毕，下次计划于{nextdatetime}启动'
            else:
                #任务执行中失败
                self.threads[name]['errors'] += 1
                if self.threads[name]['errors']  <= self.threads[name]['retry'][0]:
                    #调整下次执行的间隔为重试间隔
                    interval = self.threads[name]['retry'][1]
                    info = F'”{name}“任务执行失败，将在{interval/60}分种后重启...'
                else:
                    info = F'”{name}“任务已失败{self.threads[name]["errors"]}次，不再重试，将在下次计划时间（{nextdatetime}）启动。'
                    self.threads[name]['errors'] = 0
        else:
            #生成任务执行的时间间隔
            interval, nextdatetime = Schedule.get_interval(self.threads[name]['schedule'])
            nextdatetime = time.strftime("%m月%d日%H:%M", nextdatetime)
            info = F'“{name}”任务注册完成，按计划将于{nextdatetime}首次执行'

        print(info,'\r\n----------------------------\r\n')
        #按上面生成的时间间隔，设置本方法线程在计划时间后运行相应任务
        self.threads[name]['handle'] = Timer(interval, self._run_thread, args=(name, True))
        self.threads[name]['handle'].start()
        return None


    def close_threads(self) -> None:
        '''
        取消所有线程，退出程序前调用
        '''
        for thread in self.threads.values():
            if thread['handle']:
                thread['handle'].cancel()
        return None


    @staticmethod
    def get_interval(schedule:list[tuple]) -> tuple:
        """
        根据计划schedule（元组列表），计算到下次计划间隔的秒数。
        
        :param:
            schedule：执行任务的计划表，是两个元素的元组列表。如
                [ ('6,7', '09:00, 14:00, 17:00'), 
                  ('1,5', '08:30, 10:30, 13:30, 15:30, 17:30, 20:00'), 
                  ('3', '3600, 06:00, 22:00') ]
                具体实现的功能和含义见下面config.ini文件中样式说明，
                用ConfigParser实例的items(“my_schedule”)方法读出即是上面schedule格式
                                
                （config.ini文件格式）
                # -*- coding:utf_8 -*-
                [my_schedule]
                #一星期内每天配置不同的计划方式，按星期循环
                #等号左边代表星期几，1代表星期一，7代表星期日，星期几若重复，后面会覆盖前面的设置

                #定点执行：要求HH:MM格式，且从小到大排序
                6,7 = 09:00, 14:00, 17:00
                1,5 = 08:30, 10:30, 13:30, 15:30, 17:30, 20:00    

                #间隔执行：3600秒执行一次，仅在06:00——22:00之间执行
                3 = 3600, 06:00, 22:00
                
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
        #print("整理后的格式为：", schedule)
        '''
            [ (1, ['08:30', '10:30', '13:30', '15:30', '17:30', '20:00']), 
              (3, ['3600', '06:00', '22:00']), 
              (5, ['08:30', '10:30', '13:30', '15:30', '17:30', '20:00']), 
              (6, ['09:00', '14:00', '17:00']), 
              (7, ['09:00', '14:00', '17:00']) ]
        '''

        #获取当前时间戳，星期几，日期，时间
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