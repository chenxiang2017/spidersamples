import urllib
import time
import re
import tool
import types
from bs4 import BeautifulSoup

class Page:
	def __init__(self):
		self.tool = tool.Tool()

	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d',time.localtime(time.time()))

	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

	def getPageByUrl(self,url):
		try:
			req = urllib.request.Request(url)
			response = urllib.request.urlopen(req)
			return response.read().decode('utf-8')
		except urllib.request.URLError as e:
			if hasattr(e, 'code'):
				print(self.getCurrentTime(),u"获取问题页面失败，错误代号:",e.code)
				return None
			if hasattr(e, 'reason'):
				print(self.getCurrentTime(),u"获取问题页面失败，原因:",e.reason)
				return None

	def getOtherAnswers(self,page):
		soup = BeautifulSoup(page)
		tags = soup.select("div.answer-info")
		answers=[]
		if len(tags) > 0:
			for tag in tags:
				ansTexttags= tag.find(attrs={"class":"answer_text"}).find("pre")
				ansText = ansTexttags.string
				nameTags = tag.find(attrs={"class":"author_name"})
				name = nameTags.string
				ansTimeTags = tag.find(attrs={"class":"answer_t"})
				ansTime = ansTimeTags.string
				answer = [ansText,name,ansTime]
				answers.append(answer)
			return answers
		else:
			return answers

	def getGoodAnswers(self,page):
		soup = BeautifulSoup(page)
		tags = soup.select("div.good_answer")
		goodanswers=[]
		if len(tags) > 0:
			for tag in tags:
				goodansText = tag.find(attrs={'class':'answer_text'}).find("pre").string
				name = tag.find(attrs={'class':'answer_tip'}).find("a").string
				ansTime = tag.find(attrs={"class":"time"}).string
				answer=[goodansText,name,ansTime]
				goodanswers.append(answer)
			return goodanswers
		else:
			return goodanswers


	def getAnswers(self,url):
		if not url:
			url = "http://iask.sina.com.cn/b/5Rp63dQSz3.html"
		page = self.getPageByUrl(url)
		otheranswers = self.getOtherAnswers(page)
		goodanswers = self.getGoodAnswers(page)
		anses = otheranswers + goodanswers
		return anses

if __name__ == '__main__':
	page = Page()
	page.getAnswers("http://iask.sina.com.cn/b/87793.html")