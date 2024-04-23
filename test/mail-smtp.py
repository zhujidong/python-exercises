# -*- coding: utf_8 -*-

import smtplib
from email.message import EmailMessage
from email.headerregistry import Address


#继承自Message的子类MIMEPart 
msg = EmailMessage()  
  
#头部信息：标题等都可以支持中文 
msg['Subject'] = '邮件主题' 

#发件地址：使用Address类 
msg['From'] = Address( "张三丰", "test", "163.com" ) 

#收件人是多人，可以传递一个元组
#传递不同的参数方式来生成 
toto =[ Address("后勤", addr_spec="9527@qq.com"), Address("自己", "test", "163.com") ]
msg['To'] = toto 
 
#或者传入逗号分隔的邮件地址 
#msg['To'] = ', '.join( addrlist ) 

#msg.preamble = '这个属性会捣乱，没有被编码' 
'''	官方示例中的，但当使用add_alternative和add_attachment（即MIME 
	类型内容）时，这个属性值要被序列化，但又没有被编码，所以会报错。
	UnicodeEncodeError: 'ascii' codec can't encode character...not in range(128)
	是BUG吗？
''' 

#邮件正文：纯文本内容 
msg.set_content("邮件的正文，\r\n显示纯文件内容。") 

#替代传统的html邮件
htmls = "<html><head>HTML型邮件</head><body>\
	<p>当支持时，显示此内容，不显示上面纯文本</p></body></html>" 

msg.add_alternative( htmls, subtype="html" ) 

#准备添加附件：读取附件内容和属性：支持中文
with open('中文名.pdf','rb') as f:   
	file_data = f.read()   
	file_name = f.name 

#添加附件 
msg.add_attachment(  
	file_data, 
	maintype = 'application', 
	subtype = 'octet-stream', 
	filename = file_name
) 
''' 
add_attachment需在add_alternative后面，因为它们增加内容时，如果需要，
会修改Content-Type类型。而add_alternative在后面却要修改主段的类型mixed为alternative是不对的。 
''' 

ss = smtplib.SMTP_SSL( 'smtp.163.com', '465' )
ss.login( 'test@163.com', 'ppaasswwoorrdd' )

#缺省时，会从msg读取发件人和收件人信息
ss.send_message(msg)
ss.quit()