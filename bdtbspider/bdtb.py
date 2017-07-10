import urllib.request
import re
import codecs
from tool import Tool

class BDTB:

	def __init__(self,baseUrl,seeLZ,floorTag):
		self.baseUrl = baseUrl
		self.seeLZ = '?see_lz=' + str(seeLZ)
		self.tool = Tool()
		self.file = None
		self.floor = 1
		self.defaultTitle = u"百度贴吧"
		self.floorTag = floorTag

	def getPage(self,pageNum):
		try:
			url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
			request = urllib.request.Request(url)
			response = urllib.request.urlopen(request)
			html = response.read()
			return html
		except urllib.request.URLError as e:
			if hasattr(e, 'reason'):
				print(u'连接百度贴吧失败，错误原因',e.reason)
				return None
	def getTitle(self,html):
		'''获取帖子标题'''
		pattern = re.compile('''<h3 class="core_title_txt.*?>(.*?)</h3>''',re.S)
		html = html.decode('utf-8')
		result = re.search(pattern, html)
		if result:
			# print(result.group(1))
			return result.group(1).strip()
		else:
			return None

	def getPageNum(self,html):
		'''获取总的页数'''
		pattern = re.compile('''<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>''',re.S)
		html = html.decode('utf-8')
		result = re.search(pattern, html)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getContent(self,html):
		'''获取帖子内容'''
		pattern = re.compile('''<div id="post_content_.*?>(.*?)</div>''',re.S)
		html = html.decode('utf-8')
		items = re.findall(pattern, html)
		contents=[]
		for item in items:
			content = "\n" + self.tool.replace(item) +"\n"
			contents.append(content)
		return contents

	def setFileTitle(self,title):
		'''设置写入文件名'''
		if title is not None:
			self.file = open(title+".txt","w+",encoding = "utf-8")
		else:
			self.file = open(self.defaultTitle+".txt","w+",encoding = "utf-8")

	def writeData(self,contents):
		'''写入数据'''
		for item in contents:
			if self.floorTag == '1':
				floorLine = "\n" + str(self.floor) + u"--------------------\n"
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print(u"URL已失效，请重试")
			return
		try:
			print(u"共有"+str(pageNum)+u"页")
			for i in range(1,int(pageNum)+1):
				print(u"正在写入第"+str(i) + u"页数据")
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError as e:
			print(u"写入异常，原因："+ e.message)
		finally:
			print(u"写入完成")