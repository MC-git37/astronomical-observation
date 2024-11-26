import sqlite3
#连接
conn=sqlite3.connect('C:/Users/Administrator/Desktop/optimize7-25/DATABASE/database.db')
c=conn.cursor()
#看一看DB文件里有哪些表
c.execute("select * from sqlite_master").fetchall()
#正常执行SQL查询
c.execute("select * from table").fetchall()
#关闭

c.close()
conn.close()
