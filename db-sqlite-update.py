# -*- coding:utf_8 -*-

import sqlite3
import os.path

conn = sqlite3.connect( os.path.join(os.path.dirname(__file__), "zzz.db3" ) )
cursor = conn.cursor()


nid_list = [ '10747', 10746, 10743 ] #字符串与整形都可以
nid_tuple_list = [ ]
for t in nid_list:
        nid_tuple_list.append( [ t]  )
print( nid_tuple_list)
cursor.executemany( 'UPDATE notices SET sent=34 WHERE noticeid=?;',  nid_tuple_list[:2]  )
print( list(cursor) )

cursor.execute( 'SELECT noticeid,sent FROM notices WHERE noticeid=?;', (10746,) )

tuple_list = list( cursor )

cursor.close()
conn.commit()
conn.close()

print( tuple_list )



