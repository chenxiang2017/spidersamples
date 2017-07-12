import pymysql
import time
from log import Log

class Mysql:

    def __init__(self):
    	self.log = Log()

    def connectDb(self):
    	self.db = pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='',db='iask',charset="utf8")
    	self.cur = self.db.cursor()

    def creatTable(self):
    	self.connectDb()
    	self.cur.execute("DROP TABLE IF EXISTS iask_questions")
    	self.cur.execute("DROP TABLE IF EXISTS iask_answers")

    	ans_sql = """CREATE TABLE IF NOT EXISTS iask_answers (
    	id int(11) NOT NULL AUTO_INCREMENT primary key,
    	anstext text NOT NULL,
    	question_id int(18) NOT NULL,
    	answerer varchar(255) NOT NULL,
    	datestr varchar(255) NOT NULL)engine=innodb charset utf8"""

    	question_sql = """CREATE TABLE IF NOT EXISTS iask_questions (
    	id int(11) NOT NULL AUTO_INCREMENT primary key,
    	questext text NOT NULL,
    	questioner varchar(255) NOT NULL,
    	quesdate date NOT NULL,
    	ans_num int(11) NOT NULL,
    	url varchar(255) NOT NULL)engine=innodb charset utf8"""

    	self.cur.execute(ans_sql)
    	self.cur.execute(question_sql)
    	self.closeDb()
    	
    def closeDb(self):
    	self.cur.close()
    	self.db.close()

    def insertData(self,table,datadict):
    	self.connectDb()
    	try:
    		cols = ','.join(datadict.keys())
    		values = '","'.join(datadict.values())
    		sql = """INSERT INTO %s (%s) VALUES(%s)""" % (table,cols,'"' + values+'"')
    		print(sql)
    		try:
    			result = self.cur.execute(sql)
    			insertid = self.db.insert_id()
    			self.db.commit()
    			if result:
    				return insertid
    			else:
    				return 0
    		except Exception as e:
    			print(e)
    			self.db.rollback()
    	except Exception as e:
    		print(e)
    	finally:
    		self.closeDb()

if __name__ == '__main__':
	mysql=Mysql()
	# mysql.creatTable()
	import re
	ansNum = re.findall(r'([0-9]+)',"1回答",re.MULTILINE)
	strNum = ''.join(ansNum)
	# num = (int)ansNum
	# print(num)
	ques_dict={
				"questext":"凤凰快乐驿栈吊脚楼",
				"questioner":"chen",
				"quesdate":"2017-07-12",
				"ans_num":strNum,
				"url":"wwww"
				}
	# all_ans_dict={
	# 				"anstext":"1asdfasdf",
	# 				"question_id":"1",
	# 				"answerer":"chen",
	# 				"datestr":"2017-07-02"
	# 				}
	# mysql.insertData("iask_questions", ques_dict)