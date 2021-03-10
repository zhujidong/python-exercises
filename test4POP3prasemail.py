#!/usr/bin/python3
# -*- coding: utf_8 -*-


import poplib

from email.parser import BytesHeaderParser, BytesParser, Parser
from email.policy import default

#连接服务器
pp = poplib.POP3_SSL( 'pop.163.com', '995' )
pp.set_debuglevel(1)
print( pp.getwelcome().decode('utf_8') )

#用户权限认证
pp.user('test@163.com' )
pp.pass_( 'wwwooorrrddd' )

#邮件数量
msgnum = pp.stat()[0]
#读取邮件内容（索引从1开始，最大的最新）
mail_lines = pp.retr(msgnum)[1]
pp.close()


#开始解析

#从服务器中读出的是字节列表，下面先合成一个字节串
mail_bytes = b'\r\n'.join(mail_lines)
#从字节串生成 EmailMessage 消息类
msg = BytesParser(policy=default).parsebytes( mail_bytes )
'''
下面这种只是多了一个由字节解码为字符的过程，无意义
mail_str = b'\r\n'.join(mail_body).decode( 'utf_8' )
msg = Parser(policy=default).parsestr( mail_str )
'''

print( '邮件主题->> {}'.format( msg['Subject']) )
print( '日期->> {}'.format( msg['Date'].datetime ) )
#返回的是 发件人名称<电子邮件地址> 形式
print( '发件人->> {}'.format(msg['From']) )
print( '主类型->> {}'.format(msg['Content-Type']) )

#得到MIME段
text = msg.get_body(preferencelist=('related', 'html', 'plain'))
print( text.get_content() )

'''
#返回的是 Address类的元组:
#(Address(display_name='朱继东', username='cometear', domain='163.com'),)
print( msg['To'].addresses )

#访问元组的一个元素的值
print( msg['From'].addresses[0].addr_spec )
print( msg['To'].addresses[0].display_name )
print( msg['To'].addresses[0].username )
print( msg['To'].addresses[0].domain )

#深度优先顺序遍历信息对象树的所有部分和子部分
for part in msg.walk(): 
    print(part.get_content_type()) 

#得到MIME段
get_body(preferencelist=('related', 'html', 'plain'))

print( msg.get_body())
'''



