from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
app=Flask(__name__)  

def getDb():
	db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='dingdian',charset="utf8")
	return db
def getCursor(db):
	cur = db.cursor()
	return cur
def closedb(cur,db):
	cur.close()
	db.close()

@app.route('/') 
def index():
	db =getDb()
	cur = getCursor(db)
	cur.execute("SELECT distinct category FROM novel")
	result = cur.fetchall()
	if result is None:
		categories = {'category':None}
	else:
		categories = ((row[0]) for row in result)
	data = {'categories':categories}
	closedb(cur,db)
	return render_template('index.html',categories = data)

@app.route('/show_category/<category>')
def show_category(category):
	db = getDb()
	cur =getCursor(db)
	cur.execute("select booktitle from novel where category='"+category+"'")
	result = cur.fetchall()
	if result is None:
		books = {'book':None}
	else:
		books = (row[0] for row in result)
	data = {'books':books}
	closedb(cur, db)
	return render_template('books.html',books=data)

@app.route('/list_books/<book>')
def list_books(book):
	db = getDb()
	cur =getCursor(db)
	cur.execute("select status,chaptertitle from novel where booktitle='"+book+"'")
	result = cur.fetchall()
	if result is None:
		results = {'results':None}
	else:
		results = ((row[0],row[1]) for row in result)
	data = {'results':results}
	closedb(cur, db)
	return render_template('chapters.html',chapters=data)

if __name__ == '__main__':  
    app.run(host="127.0.0.1",port=8888,debug=True)