# -*- coding:utf_8 -*-

import time

from mailhelper import MailHelper, ImapHelper




if __name__ == '__main__':

    with ImapHelper() as m:
        today = time.strftime('%d-%b-%Y')
        wht = m.get_mails('BODY[HEADER]', F'(SINCE "{today}")')
    for w in wht:
        t = m.trans_header(w)
        print(t.get('subject'), t.get('from'))

