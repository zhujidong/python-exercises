# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''


import time
from threading import Timer


class Schedule(object):
    '''
    管理计划任务；每个任务以线程方式运行。
    
    主要方法：
    reg_thread（），注册一个任务，即可按计划运行此任务。
    list_threads(),列出已经注册的任务名称和计划表
    close_threads(),关闭所有线程，退出主程序时调用此方法。
    pause_thread()，按名字暂停某个任务。
    restart_thread()，恢复某个任务的执行

    '''

    def __init__(self) -> None:

        self.threads = {}
        '''
        记录reg_thread（）时所有计划任务线程的信息，key为给任务起的“名字”.
        value也是一个字典,记录线程相关信息，相关信息见reg_thread()。

        '''

    def reg_thread( self, name:str, fun:object, param:tuple, schedule:dict) -> None:
        '''
        将一个方法函数，注册为一个计划任务

        :param:
            name:str,为计划任务的起的名称，暂停、重启或立即执行此任务需用此名字索引，也是self.threads的key
            
            fun:str,要注册成任务线程的函数方法。
                *要求此方法返回一个元组，第一个元素为任务状态码，0,正常；第二个元素为任务相关信息（错误信息等）
                *本方法中只能传给任务函数位置参数
            param:tuple,任务线程的参数，**只能传递位置参数给fun **

            schedule:dict,任务执行的计划，定义方式见config.ini和config.toml
                sche:[
                    (1, ['600', '06:00', '22:00']), 
                    (3, ['09:00', '14:00', '17:00']), 
                    (7, ['08:30', '10:30', '13:30', '15:30', '17:30', '20:00']) ],
                retry:[1,300], #线程执行失败时，重试次数与时间间隔（默认重试1次，隔300秒后重试）
                run_now:bool 计划划任务注册后是否立即执行一次，否则按计划执行

        '''
        schedule = Schedule._trans_schedule(schedule)
        self.threads[name] = {  'fun':fun, 'param':param, 'schedule':schedule,
                                'errors':0, 'handle':None, 'statu':1    }
        '''
        serf.threads以计划名字name为key, value仍是字典，其它key含义如下
        errors:int,记录线程执行失败次数
        handle:线程的句柄，取消、重启，立即执行任务等使用
        statu:int, 计划任务的状态，是否按计划执行1,正常, 0 暂停 
        '''
        self._run_thread(name, schedule['run'])
        return None


    def _run_thread(self, name, run_now=True) -> None:
        '''
        调用Timer启动线程，每个线程就是一个等待下次计划时间运行的任务

        :param:
            name:str,要执行的任务名称
            run_now:bool,为真时，立即运行任务而不管计划，然后设置下次计划时间运行
                         为假时，读取计划，设置计划时间运行。
                    *当此方法按计划调用自身时，通常为真，因为是到了计划时间才调用的，当然要运行任务
                    *通常是给注册任务时使用，看是否当即运行一次，还是按计划时间运行
        '''
        
        #立即运行任务而不管计划，然后求出下次计划时间
        if run_now:
            now = time.strftime("%m月%d日%H:%M", time.localtime(time.time()))
            print(F'\r\n----------------------------\r\n{now}：”{name}“任务启动...')
            
            #运行计划的任务，成功返回真。      *此处只将元组展开成位置参数给要执行的方法*
            rs, stdout = self.threads[name]['fun'](*self.threads[name]['param'])
                        
            #调用方法生成到下次的执行任务的间隔秒数
            interval, nextdatetime = Schedule._get_interval(self.threads[name]['schedule'])
            nextdatetime = time.strftime("%m月%d日%H:%M", nextdatetime)

            #根据任务执行的返回结果，调整下次执行间隔和提示信息
            if rs==0:
                self.threads[name]['errors'] = 0
                info = F'“{name}”任务执行完毕:{stdout}，\n下次计划于{nextdatetime}启动'
            #任务执行中失败,且要求重试
            elif self.threads[name]['schedule']['retry'][0]>0:
                self.threads[name]['errors'] += 1
                #没达到重试次数，调整下次执行的间隔为重试间隔
                if self.threads[name]['errors']  <= self.threads[name]['schedule']['retry'][0]:
                    interval = self.threads[name]['schedule']['retry'][1]
                    info = F'”{name}“执行失败：{stdout}\n 任务将在{interval/60}分种后重启...'
                else:
                    info = F'”{name}“任务已失败{self.threads[name]["errors"]}次，不再重试，将在下次计划时间（{nextdatetime}）启动。'
                    self.threads[name]['errors'] = 0
                    #发送错误报告？
            else:
                info = F'”{name}“执行失败：{stdout}...\n 将在下次计划时间（{nextdatetime}）启动。'
                #发送错误报告？

        #非立即运行的任务，调用得到时间间隔即可
        else:
            interval, nextdatetime = Schedule._get_interval(self.threads[name]['schedule'])
            nextdatetime = time.strftime("%m月%d日%H:%M", nextdatetime)
            info = F'“{name}”任务将按计划将于{nextdatetime}运行。'

        #实际是把自己生成一个线程，调用被注册的计划任务
        print(info,'\r\n----------------------------\r\n')
        self.threads[name]['handle'] = Timer(interval, self._run_thread, args=(name, True))
                                       #计划时间后才运行，所以通常给本方法传递true以立即运行任务
        self.threads[name]['handle'].start()
        return None


    def pause_thread(self, name) -> str:
        '''
        暂停某个计划的任务
        '''
        info = 0
        if name in self.threads.keys():
            self.threads[name]['handle'].cancel()
            self.threads[name]['statu'] = 0
            info = F'"{name}"任务已暂停。'
        else:
            info = F'"{name}"任务不存在。'
        return info

    def restart_thread(self, name) -> None:
        ''' 重启某个计划的任务 '''
        info = 0
        if name in self.threads.keys() and self.threads[name]['statu']==0:
            self.threads[name]['statu'] = 1
            self._run_thread(name, run_now=False)
            info = F'"{name}"任务重启完成。'
        else:
            info = F'"{name}"任务不存在或状态正常不用重启。'
        return info


    def run_thread(self, name) -> str:
        ''' 立即运行一次某个已注册的任务 '''
        info = 0
        if name in self.threads.keys():
            #不取消就会多一个线程,且handle被这次新的覆盖而失去控制
            self.threads[name]['handle'].cancel()
            self.threads[name]['statu'] = 1 #如果的暂停的任务,会变为正常
            self._run_thread(name, run_now=True)
            info = F'"{name}"立即运行任务完成。'
        else:
            info = F'"{name}"任务不存在。'
        return info


    def list_threads(self) -> None:
        ''' 列出运行的计划任务信息 '''
        for key, value in self.threads.items():
            print(key,'状态:', '正常' if value['statu']==1 else "暂停")
            print(value['schedule'])


    def close_threads(self) -> None:
        ''' 取消所有线程，退出程序前调用 '''
        for thread in self.threads.values():
            if thread['handle']:
                thread['handle'].cancel()
        return None


    @staticmethod
    def _get_interval(schedule:dict) -> tuple:
        '''
        根据计划schedule（元组列表），计算现在到下次计划间隔的秒数。
        
        :param:
            schedule：执行任务的计划表，定义方法见reg_thread（）
            
        :return:            
            至下次计划的间隔秒数, 下次计划的日期时间
        '''

        schedule = schedule['sche']

        #获取当前时间戳，星期几，日期，时间
        stamp = time.time()
        struct = time.localtime(stamp)
        day_of_week = struct[6] + 1 # 1,周一；7，周日        
        date_ = time.strftime("%Y-%m-%d", struct)
        time_ = time.strftime("%H:%M", struct)

        #提取当天的计划列表 和 下一天任务是星期几和对应计划列表
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
        #当天有计划，并且是定点执行的
        if table and ':' in table[0]:
            for tb in table:
                if tb > time_:
                    next_stamp = time.mktime(time.strptime(F'{date_} {tb}', '%Y-%m-%d %H:%M'))  
                    break
        #当天有计划，是按时间间隔执行
        elif table:
            next_stamp = stamp + int(table[0])
            next_time = time.strftime("%H:%M", time.localtime(next_stamp))
            #下个计划没到当天计划开始时间
            if next_time <=  table[1]:
                next_stamp = time.mktime(time.strptime(F'{date_} {table[1]}', '%Y-%m-%d %H:%M'))  
            #超计划的时间段了，不是今天的计划了
            elif next_time >= table[2]:
                next_stamp =None

        #当天没有计划或当天计划的时间之外
        if next_stamp is None:
            #设置计划为下一个天的开始时间就可
            if ':' in next_table[0]:
                next_time = next_table[0]
            else:
                next_time = next_table[1]

            #下个计划天与今天相距的天数
            if next_day_of_week <= day_of_week:
                next_day_of_week += 7
            days = next_day_of_week - day_of_week

            # 用 今日 和 下次计划时间 生成的时间戳，再加上相差天数的的秒数，即为下次计划的时间戳。
            next_stamp = time.mktime(time.strptime(F'{date_} {next_time}', '%Y-%m-%d %H:%M'))  
            next_stamp += days*24*3600

        interval = next_stamp - stamp
        return interval, time.localtime(next_stamp)


    @staticmethod
    def _trans_schedule(config:dict) -> dict:
        '''
        配置文件读出的字典，整理出使用的格式，见reg_thread（）

        :param:
            config:dict,计划配置的字典，可以从配置文件中读取
        
        :return:dict，三个键：计划时间，重试规则，是否立即运行
            sche: #计划时间
                [(1, ['600', '06:00', '22:00']), 
                 (3, ['09:00', '14:00', '17:00']), 
                 (7, ['08:30', '10:30', '13:30', '15:30', '17:30', '20:00']) ],
            retry:[1,300], #线程执行失败时，重试次数与时间间隔（默认重试1次，隔300秒后重试）
            run_now:bool 计划划任务注册后是否立即执行一次，否则按计划执行
        '''

        sche = {} #计划任务
        retry = [1, 300] #重试规则[次数，间隔秒数]
        run = False
        week = ['1','2','3','4','5','6','7']

        for key, value in config.items():
            if key=='run':
                #toml读的布尔型
                if type(value)==bool: 
                    run = value
                #toml或ini读的字符型，只要不是大小写的true，就为假
                elif type(value)==str and value.strip().lower()=='true':
                    run = True
            elif key=='retry':
                #从toml读取的列表，并且有两个元素
                if type(value)==list and len(value)==2: 
                    retry = value
                #如果是乱七八糟的字符串
                elif type(value)==str:
                    r = value.replace(' ','').split(",")
                    if len(r)==2 and r[0].isdigit() and r[1].isdigit():
                        retry = [int(r[0]), int(r[1])]
            else:
                #去除空格，如果不是列表，转化为列表
                if type(value)==list:
                    value =[v.replace(' ', '') for v in value]
                else:
                    value = value.replace(' ','').split(",")

                split_key = key.replace(' ','').split(",")
                for skey in split_key:
                    if skey in week:
                        sche[int(skey)] = value
        #排序，生成列表
        sche = sorted(sche.items(), key=lambda x:x[0])
        schedule = {'sche':sche, 'retry':retry, 'run': run}

        return schedule
