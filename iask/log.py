import time

class Log:
	def __init__(self):
		pass

	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d',time.localtime(time.time()))