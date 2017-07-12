from urllib.request import Request,urlopen,URLError
import urllib.request
import re
import sys
from bs4 import BeautifulSoup
from log import Log
from page import Page
from mysql import Mysql

class IAskSpider:

	def __init__(self):
		self.page_num = 1
		self.total_num = None
		self.page_spider = Page()
		self.mysql = Mysql()
		self.log = Log()

	def getPageUrlByNum(self,page_num):
		url = "http://iask.sina.com.cn/c/180-all-"+str(page_num)+"-new.html"
		return url

	def getPageByNum(self,page_num):
		url = self.getPageUrlByNum(page_num)
		print(url)
		req = Request(url)
		try:
			response = urlopen(req)
		except URLError as e:
			if hasattr(e, "code"):
			    print(self.log.getCurrentTime(),u"获取页面失败，错误代号：",e.code)
			    return None
			if hasattr(e, "reason"):
				print(self.log.getCurrentTime(),u"获取页面失败，原因：",e.reason)
				return None
		else:
			html = response.read()
			html = html.decode("utf-8")
			return html

	def getTotalPageNum(self):
		print(self.log.getCurrentTime(),u"正在获取页面个数，请稍后。。。")
		page = self.getPageByNum(1)
		soup = BeautifulSoup(page)
		tags = soup.find_all('div',attrs={'class':'page'})
		num = tags[0]['pagecount']
		if num:
			return num
		else:
			print(self.log.getCurrentTime(),u"获取总页面失败")
			return None

	def getQuestionInfo(self,item):
		author = item.find('img').get('alt')
		href = item.find(attrs={'class':'question-title'}).find('a').get('href')
		title = item.find(attrs={'class':'question-title'}).find('a').string
		others = item.find(attrs={'class':'queation-other'}).find_all('span')
		ans_num = others[0].string
		ans_time = others[1].string
		return [author,href,title,ans_num,ans_time]

	def getQuestions(self,page_num):
		page = self.getPageByNum(page_num)
		soup = BeautifulSoup(page)
		lists = soup.find_all(attrs = {'class':'list'})
		for item in lists:
			info = self.getQuestionInfo(item)
			if info:
				url = "http://iask.sina.com.cn" + info[1]
				anses = self.page_spider.getAnswers(url)
				print("---------------------------------------------------------------------------------------------------")
				print(self.log.getCurrentTime(),u"当前爬取第",page_num,u"页的内容,发现一个问题",info[2],u"回答数",info[3])
				ansNum = re.findall(r'([0-9]+)',info[3],re.MULTILINE)
				ans_Num = ''.join(ansNum)
				ques_dict={
				"questext":info[2],
				"questioner":info[0],
				"quesdate":info[4],
				"ans_num":ans_Num,
				"url":url
				}
			insert_id = self.mysql.insertData("iask_questions",ques_dict)
			print(self.log.getCurrentTime(),u"保存到数据库，此问题ID为",insert_id)
			if len(anses) > 0:
				print(self.log.getCurrentTime(),insert_id,u"号问题的答案")
				for ans in anses:
					print(self.log.getCurrentTime(),insert_id,u"号问题的所有答案开始保存")
					all_ans_dict={
					"anstext":ans[0],
					"question_id":str(insert_id),
					"answerer":ans[1],
					"datestr":ans[2]
					}
					if self.mysql.insertData("iask_answers", all_ans_dict):
						print(self.log.getCurrentTime(),u"保存答案成功")
					else:
						print(self.log.getCurrentTime(),u"保存答案失败")
			print("-----------------------------------------------------------------------------------")

	def main(self):
		f_handler = open("out.log","w",encoding="utf-8")
		sys.stdout = f_handler
		page = open("page.txt","r",encoding="utf-8")
		content = page.readline()
		if len(content) > 0:
			start_page = int(content.strip()) - 1
		else:
			self.total_num = self.getTotalPageNum()
			start_page = self.total_num
		page.close()
		print(self.log.getCurrentTime(),"开始页码",start_page)
		print(self.log.getCurrentTime(),"爬虫正在启动，开始爬去爱问知识人问题")
		print(self.log.getCurrentTime(),u"获取到页面个数",self.total_num,"个")
		start_page = int(start_page)
		for x in range(1,start_page):
			page_num = start_page-x+1
			print(self.log.getCurrentTime(),"正在抓取第",page_num,"个页面")
			try:
				self.getQuestions(page_num)
			except urllib.request.URLError as e:
				if hasattr(e, "reason"):
					print(self.log.getCurrentTime(),"某总页面内抓取或提取失败,错误原因",e.reason)
			except Exception as e:
				print(self.log.getCurrentTime(),"某总页面内抓取或提取失败,错误原因:",e)

			if page_num < start_page:
				f=open("page.txt","w",encoding="utf-8")
				f.write(str(page_num))
				print(self.log.getCurrentTime(),"写入新页码",page_num)
				f.close()

if __name__ == '__main__':
	iaskspider = IAskSpider()
	iaskspider.main()