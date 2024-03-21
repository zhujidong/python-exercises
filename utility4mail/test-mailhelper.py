# -*- coding:utf_8 -*-

import os
import sys
import time
from configparser import ConfigParser

from mailhelper import MailHelper, ImapHelper

def master_order():
    config = ConfigParser()
    config.read( os.path.join(sys.path[0], "mail.ini"), encoding='utf_8')
    master = config['mail']['master']
    
    #读取今天的邮件，只取最新的13个
    with ImapHelper() as m:
        #today = time.strftime('%d-%b-%Y')
        today = "15-Mar-2024"
        bmails = m.get_mails('BODY[HEADER]', F'(SINCE "{today}")', 13)

    order = []
    for bmail in bmails:
        hd = m.trans_header(bmail)
        mail_time = hd.get('Date')
        struct_t = time.strptime(mail_time, "%a, %d %b %Y %H:%M:%S +0800")
        mail_sec =time.mktime(struct_t)
        now = time.time()
        if (now-mail_sec)/60 < 13500:
            mail_from = hd.get('From')
            if master in mail_from:
                order.append(hd.get('Subject'))
    print(order)

def base_test():
    with ImapHelper() as m:
        #today = time.strftime('%d-%b-%Y')
        today = "15-Mar-2024"
        wht = m.get_mails('BODY[HEADER]', F'(SINCE "{today}")')
    for w in wht:
        t = m.trans_header(w)
        print(t.get('Subject'))
        ttt = t.get('Date')
        print(type(ttt),ttt)
   

if __name__ == '__main__':

    #base_test()
    
    master_order()