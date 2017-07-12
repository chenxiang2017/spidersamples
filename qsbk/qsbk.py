import urllib.request
import re

class QSBK:

	def __init__(self):
		self.pageIndex = 1
		self.user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		self.headers = {'User-Agent':self.user_agent}
		self.stories = []
		self.enable = False

	def getPage(self,pageIndex):
		try:
			baseurl = ' http://www.qiushibaike.com/hot/page/'
			url = baseurl+ str(pageIndex)
			request = urllib.request.Request(url,headers = self.headers)
			response = urllib.request.urlopen(request)
			html = response.read().decode('utf-8')
			return html
		except urllib.request.URLError as e:
			if hasattr(e, "reason"):
				print(u"连接糗事百科失败，错误原因：",e.reason)
				return None

	def getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print(u"页面加载失败....")
			return None
		pattern = re.compile("""<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats">.*?<i class="number">(.*?)</i>.*?</span>""", re.S)
		items = re.findall(pattern, pageCode)
		pageStories = []
		for item in items:
			author = item[0]
			content = item[1]
			image = item[2]
			haoxiaonum = item[3]
			haveImg = re.search("img", image)
			if not haveImg:
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR, "\n", content)
				pageStories.append([author.strip(),text.strip(),content.strip(),haoxiaonum.strip()])
		return pageStories

	def loadPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def getOneStory(self,pageStories,pageIndex):
		for story in pageStories:
			inputstr = input()
			self.loadPage()
			if inputstr == "Q":
				self.enable = False
				return
			print(u"第%d页\t 发布人:%s\t 发布内容:%s\t 好笑:%s \n" %(pageIndex,story[0],story[2],story[3]))

	def start(self):
		print(u"正在读取糗事百科，按回车查看新段子,Q退出")
		self.enable=True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)





























