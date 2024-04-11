# -*- coding:utf_8 -*-

import time
from os import path as ospath
from sys import path as syspath
from mailhelper import ImapHelper, SmtpHelper

if __name__ == '__main__':
    #将上级目录加入sys.path, 才能找到同级目录内的包
    syspath.append(ospath.dirname(ospath.dirname(__file__)))
    from configreader.tomlreader import TOMLReader

    config= TOMLReader()

    def imap_test():
        with ImapHelper(config['mailhelper']) as imap:
            #today = time.strftime('%d-%b-%Y')
            today = "03-Apr-2024"
            wht = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")', 2)
    
        for w in wht:
            t = imap.parse_header(w)
            print(t['Subject'])
            print(t['From'].addresses[0].addr_spec)
            print(t['date'].datetime)

    def smtp_test():
        with SmtpHelper(config['mailhelper']) as smtp:
            smtp.send_mail( 
                config['receiver'], 
                '多收件人',
                '这是使用\nsend_message发送'
            )

    imap_test()
    #smtp_test()