from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
app=Flask(__name__)  

@app.route('/')  
def index():
	db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='dingdian',charset="utf8")
	cur = db.cursor()
	cur.execute("SELECT * FROM novel")
	result = cur.fetchall()
	print(result)

	# if result is None:
	# 	json_result = {'id':None}
	# 	return json.dumps(json_result, ensure_ascii=False)
	# else:
	# 	json_result = {'id':result.id,'category':result.category}
	# 	return json.dumps(json_result,ensure_ascii=False)
	return render_template('index.html')

if __name__ == '__main__':  
    app.run(host="127.0.0.1",port=8888,debug=True)