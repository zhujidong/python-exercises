# -*- coding:utf_8 -*-

import sqlite3

import time
import os.path

conn = sqlite3.connect( os.path.join(os.path.dirname(__file__), "zzz.db3" ) )
cursor = conn.cursor()


'''    当select 使用 where in( ) 时
'''
#nid_list = [ '10747', 10746, 10743 ] #字符串与整形都可以

#以下两种方法都可以，总之，自己生成 in(   ) 里面的 ？ 个数。
#cursor.execute( f"SELECT * FROM notices WHERE noticeid in ({ ','.join( ['?']*len(nid_list) ) }) ;", nid_list )
#cursor.execute( f"SELECT * FROM notices WHERE noticeid in ({ ('?,'*len(nid_list))[:-1] }) ;", nid_list )

#以本地时间为准2天前（48小时）的时间  
#cursor.execute( f"SELECT noticeid,pubdate FROM notices WHERE  pubdate > datetime('now', 'localtime', '-2 days') ;" )

date ="2021-02-10"
time.strptime(date, "%Y-%m-%d") 
cursor.execute( f"SELECT noticeid,pubdate FROM notices WHERE  date(pubdate) = '{date}';" )

tuple_list = list( cursor )

cursor.close()
conn.commit()
conn.close()

print( tuple_list )



