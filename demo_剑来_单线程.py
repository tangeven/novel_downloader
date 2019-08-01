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

    def parse(self):
        """获取每一章小说的url"""
        resp = requests.get(self.url, headers=self.headers)
        html = etree.HTML(resp.content)
        page_list = html.xpath('//div[@class="listmain"]/dl/dd')[12:]
        page_url_list = []
        for page in page_list:
            pages = {}
            page_title = page.xpath('./a/text()')[0]
            page_url = page.xpath('./a/@href')[0]
            pages['标题'] = page_title
            pages['url'] = 'https://www.biqugex.com' + page_url
            page_url_list.append(page_url)
        return page_url_list

    def get_page_content(self,page_url):
        """拿到每个章节的内容"""
        resp = requests.get(page_url, headers=self.headers)
        html = etree.HTML(resp.content)
        page_content = {}
        novel_title = html.xpath('//div[@class="content"]/h1/text()')[0]
        novel_content = html.xpath('//div[@id="content"]/text()')
        page_content['title'] = novel_title
        page_content['content'] = novel_content
        return page_content

    def save(self,novel):
        """保存在本地"""
        with open('剑来.txt','a') as f:
            f.write(novel['title'] + '\n')
            content = novel['content']
            for i in content:
                f.write(i.strip() + '\n')
            f.write('\n')
            f.write('\n')

    def run(self):
        """主程序入口"""
        page_url_list = self.parse()
        for page_url in page_url_list:
            page_url = 'https://www.biqugex.com'+page_url
            novel = self.get_page_content(page_url)
            self.save(novel)


if __name__ == "__main__":
    n = Novel()
    n.run()

