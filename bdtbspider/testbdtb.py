from bdtb import BDTB

if __name__ == '__main__':
	url = input(u"请输入帖子url:")
	# baseUrl = 'http://tieba.baidu.com/p/3138733512'
	seeLZ = input(u"是否只看楼主，是输入1，否输入0\n")
	floorTag = input(u"是否加入楼层分割线，是输入1，否输入0\n")
	bdtb = BDTB(url, seeLZ, floorTag)
	bdtb.start()
