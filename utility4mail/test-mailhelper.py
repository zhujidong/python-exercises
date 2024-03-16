# -*- coding:utf_8 -*-


from mailhelper import MailHelper, ImapHelper




if __name__ == '__main__':

    #print(MailHelper()._login_imap())
    with ImapHelper() as r:
        print(r[0].imap.select())
    print(r)
    print(r[0].imap.select())