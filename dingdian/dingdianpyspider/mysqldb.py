from six import itervalues
# import mysql.connector
import pymysql
from datetime import date, datetime, timedelta

class SQL:

    username = 'root'
    password = ''
    database = 'dingdian'
    host = 'localhost'
    connection = ''
    charset = 'utf8'
    connect = True
    placeholder = '%s'
    def __init__(self):
        if self.connect:
            SQL.connect(self)
    def escape(self,string):
        return '`%s`' % string
    def connect(self):
        config={'user':SQL.username,'password':SQL.password,'host':SQL.host,'charset':SQL.charset}
        if SQL.database != None:
            config['database'] = SQL.database
        try:
            cnx = pymysql.connect(**config)
            # cnx = mysql.connector.connect(**config)
            SQL.connection = cnx
            return True
        except Exception as err:
            print('Something went wrong',err)
    def replace(self,tablename=None,**values):
        if SQL.connection == '':
            print('Please connect first')
            return False
        tablename = self.escape(tablename)
        if values:
            _keys = ",".join(self.escape(k) for k in values)
            _values = ",".join([self.placeholder,]*len(values))
            sql_query = "REPLACE INTO %s (%s) VALUES (%s)" % (tablename,_keys,_values)
        else:
            sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename
        cur = SQL.connection.cursor()
        try:
            if values:
                cur.execute(sql_query,list(itervalues(values)))
            else:
                cur.execute(sql_query)
            SQL.connection.commit()
            return True
        except Exception as err:
            print("An error occured :{}".format(err))
            return False