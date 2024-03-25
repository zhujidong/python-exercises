# -*- coding:utf_8 -*-


import time

def imap_test():
    with ImapHelper() as imap:
        #today = time.strftime('%d-%b-%Y')
        today = "15-Mar-2024"
        wht = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")')
    
    for w in wht:
        t = imap.trans_header(w)
        print(t.get('Subject'))
        print(t.get('Date'))


def master_order():
    #读取今天的邮件，只取最新的13个
    with ImapHelper() as m:
        #today = time.strftime('%d-%b-%Y')
        today = "15-Mar-2024"
        bmails = m.get_mails('BODY[HEADER]', F'(SINCE "{today}")', 13)

    from email.utils import parseaddr
    from utility4configreader.configreader import ConfigReader
    MASTER = ConfigReader().getdict('master')

    order = []
    for bmail in bmails:
        hd = m.trans_header(bmail)
        mail_time = hd.get('Date')
        struct_t = time.strptime(mail_time, "%a, %d %b %Y %H:%M:%S +0800")
        mail_sec =time.mktime(struct_t)
        now = time.time()
        if (now-mail_sec)/60 < 13500:
            mailadd = parseaddr(hd.get('From'))[1]
            if mailadd in MASTER.values():
                order.append(hd.get('Subject'))
    print(order)



def smtp_test():
    with SmtpHelper() as smtp:
        print('smtp ok')


if __name__ == '__main__':
    
    from os import path as ospath
    from sys import path as syspath
    #将上级目录加入sys.path, 才能找到同级目录内的包
    syspath.append(ospath.dirname(ospath.dirname(__file__)))
    from mailhelper import ImapHelper, SmtpHelper
    
    imap_test()
    #master_order()
    smtp_test()