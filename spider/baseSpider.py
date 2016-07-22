#-*-coding=utf-8-*-
__author__ = 'jeffrey'
from bs4 import BeautifulSoup
from urllib import request
import gzip
import time
import random
import os


class config():
    site_url = ""
    last_page = 1
    page_url = ""
    download_path = "download"


class baseSpider():

    config  # = config()

    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
        self.headers = {"User-Agent": user_agent,
                        "Referer": "https://www.google.com"}

    def getWebContent(self, url):
        # time.sleep(3*random.random())
        req = request.Request(url, headers=self.headers)
        res = request.urlopen(req)
        charset = res.headers.get_content_charset()
        content = res.read()
        info = res.info().get("Content-Encoding")
        if info == None:
            html = content.decode(charset)
        else:
            html = gzip.decompress(content).decode(charset)
        return html

    def getBS4WebContent(self, url):
        html = self.getWebContent(url)
        bs = BeautifulSoup(html, 'html.parser')
        return bs

    def download(self, url):
        pass

    def __makeDownloadDir(self):
        sub_folder = os.path.join(os.getcwd(), self.config.download_path)
        if not os.path.exists(sub_folder):
            os.mkdir(sub_folder)
        os.chdir(sub_folder)

    def getPhoto(self):
        self.__makeDownloadDir()
        start = 0
        for i in range(start, self.config.last_page):
            url = self.config.page_url + str(i)
            # time.sleep(1)
            self.download(url)
