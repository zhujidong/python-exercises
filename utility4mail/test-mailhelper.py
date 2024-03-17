# -*- coding:utf_8 -*-


from mailhelper import MailHelper, ImapHelper




if __name__ == '__main__':

    #print(MailHelper()._login_imap())
    with ImapHelper() as m:
        m.get_mail()