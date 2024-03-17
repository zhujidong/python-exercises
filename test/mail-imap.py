# -*- coding: utf_8 -*-


import imaplib

from email.policy import default
from email.parser import BytesParser



#连接服务器；权限认证
imap = imaplib.IMAP4_SSL( 'imap.163.com', '993' )
#登录验证
print( imap.login( 'test@163.com', 'wwoorrdd' ) )

#网易服务器要求客户端发送一个ID命令，否则认为是不安全的：
#SELECT Unsafe Login. Please contact kefu@188.com for help
#imap求每条命令前有一个标签，以便异步响应，所以调用imap._new_tag()
#发送数据是字节串，所以b修饰，末尾要有\r\n，否则服务器一直在等命令结束
imap.send( b'%s ID ("name" "zgzxxbot" "version" "1.0" "vendor" "J.D.zhu")\r\n' % imap._new_tag() )

#默认参数是INBOX,返回邮件数量 
print( imap.select() )

#response是一个列表；第一个元素是‘空格分隔的邮件号’
status, response = imap.search(None, '(UNSEEN)') 
unread_msg_nums = response[0].split() 

#因为BODY[ ]相当于RFC822，所以返回的是全部邮件内容
_, response = imap.fetch( unread_msg_nums[0],  '(UID BODY[])' ) 

#从字节串生成 EmailMessage 消息类
#如果是BODY[HEADER]也可以生成这个消息实例
msg = BytesParser(policy=default).parsebytes( response[0][1] )

print( msg['Subject'])
print( msg['Date'])
#返回的是 发件人名称<电子邮件地址> 形式
print( msg['From'] )
print( msg['To'] )
print( msg['Content-Type'])

#提取纯文本内容
print( msg.get_body('plain').get_content())

imap.logout()
