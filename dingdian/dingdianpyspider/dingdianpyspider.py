#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-20 16:56:22
# Project: dingdian

from pyspider.libs.base_handler import *
import re
from bs4 import BeautifulSoup
from pyspider.result import ResultWorker
from pyspider.database.mysql.mysqldb import SQL

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        baseurl = 'http://www.x23us.com/class/'
        sufix = '_1.html'
        for i in range(1,11):
            url = baseurl + str(i) + sufix
            self.crawl(url,callback=self.index_page,validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        total_page_num = response.doc('.last').text()
        total_page_num = int(total_page_num)
        first = response.doc('.first').text()
        first = int(first)
        baseurl = 'http://www.x23us.com/class/1_'
        sufix='.html'
        for index in range(first,total_page_num+1):
            url = baseurl + str(index) + sufix
            self.crawl(url,callback=self.list_books,validate_cert=False)
                
    def list_books(self, response):
        items = response.doc('tr').items()
        for item in items:
            booktitle = item.find('.L').find('a').eq(1).text()
            if len(booktitle)==0:
                continue
            c = item.find('.C')
            author = item.find('.C').eq(0).text()
            updatetime = item.find('.C').eq(1).text()
            status = item.find('.C').eq(2).text()
            latestchapter = item.find('.L').eq(1).text()
            
            bookurl = item.find('.L').find('a').eq(1).attr('href')
            savedata = {'booktitle':booktitle,'author':author,'updatetime':updatetime,'status':status}
            self.crawl(bookurl,callback=self.list_chapter,save = savedata,validate_cert=False)
            
    def list_chapter(self,response):
        items = response.doc('.L').items()
        booktitle = response.save['booktitle']
        author = response.save['author']
        updatetime = response.save['updatetime']
        status = response.save['status']
        for item in items:
            chaptertitle = item.find('a').text()
            chapterurl = item.find('a').attr('href')
            savedata = {'booktitle':booktitle,'author':author,'updatetime':updatetime,'status':status,'chaptertitle':chaptertitle}
            self.crawl(chapterurl,callback=self.list_content,save = savedata,validate_cert=False)
    
    @config(priority=2)     
    def list_content(self,response):
        nav=response.doc('dt > a').items()
        navlist = []
        for item in nav:
            navlist.append(item.text())
        if len(navlist) > 0:
            category = navlist[1]
        items = response.doc('h1').items()
        prevnexturls = response.doc('h3').items()
        contents = response.doc('#contents').items()
        booktitle = response.save['booktitle']
        author = response.save['author']
        updatetime = response.save['updatetime']
        status = response.save['status']
        chaptertitle = response.save['chaptertitle']
        for item in contents:
            content = item.text()
        for item in prevnexturls:
            prevurl = item.find('a').eq(0).attr('href')
            nexturl = item.find('a').eq(2).attr('href')
        #for item in items:
        #    chaptertitle = item.text()
        return {
            "booktitle":booktitle,
            "author":author,
            "updatetime":updatetime,
            "status":status,
            "category":category,
            "chaptertitle":chaptertitle,
            "content":content
        }
    def on_result(self, result):
        if not result or not result['booktitle']:
            return
        sql = SQL()
        sql.replace('novel',**result)
        
        
        
        
        