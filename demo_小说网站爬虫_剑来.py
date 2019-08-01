import requests
from queue import Queue
import random
from lxml import etree
from pymongo import MongoClient
import time
import threading
import re


class Novel():
    """爬取小说网站小说，比如剑来"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/72.0.3626.119 Safari/537.36 "
        }
        self.url = 'https://www.biqugex.com/book_67088/'
        self.page_url = Queue()
        self.novel_content = Queue()

    def parse(self):
        """获取每一章小说的url,并存入队列"""
        resp = requests.get(self.url,headers=self.headers)
        html = etree.HTML(resp.content)
        page_list = html.xpath('//div[@class="listmain"]/dl/dd')[12:]
        for page in page_list:
            pages = {}
            page_title = page.xpath('./a/text()')[0]
            page_url = page.xpath('./a/@href')[0]
            pages['标题'] = page_title
            pages['url'] = 'https://www.biqugex.com'+page_url
            self.page_url.put(pages['url'])
            print(pages)

    def get_page_content(self):
        """拿到每个章节的内容"""
        while True:
            page_url = self.page_url.get()
            self.page_url.task_done()
            resp = requests.get(page_url,headers=self.headers)
            html = etree.HTML(resp.content)
            page_content = {}
            novel_title = html.xpath('//div[@class="content"]/h1/text()')[0]
            novel_content = html.xpath('//div[@id="content"]/text()')
            page_content['title'] = novel_title
            page_content['content'] = novel_content
            # print(page_content)
            self.novel_content.put(page_content)
            # with open('剑来.txt','a') as f:

    def save(self):
        """保存在本地"""
        while True:
            novel = self.novel_content.get()
            with open('剑来.txt','a') as f:
                f.write(novel['title']+'\n')
                content = novel['content']
                for i in content:
                    f.write(i.strip()+'\n')
                f.write('\n')
                f.write('\n')
            # print(novel)

    def run(self):
        t = []
        for i in range(10):
            t1 = threading.Thread(target=self.parse)
            t.append(t1)

        for i in range(10):
            t2 = threading.Thread(target=self.get_page_content)
            t.append(t2)

        for i in range(5):
            t3 = threading.Thread(target=self.save)
            t.append(t3)

        for thread in t:
            thread.start()


if __name__ == "__main__":
    n = Novel()
    n.run()
