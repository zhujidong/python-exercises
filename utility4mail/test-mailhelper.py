# -*- coding:utf_8 -*-


from mailhelper import MailHelper, ImapHelper




if __name__ == '__main__':

    #print(MailHelper()._login_imap())
    with ImapHelper() as m:
        wht = m.get_mails('BODY[HEADER]', '(FROM "mail@service.netease.com")')

    for w in wht:
        print(w.get('subject'))