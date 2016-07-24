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
    page_urls = ""
    _download_path = ""
    time_sleep = 0

    def __init__(self):
        self._download_path = os.getcwd()

    @property
    def download_path(self):
        return self._download_path


class baseSpider():
    _downloaded_photos = []
    config

    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36"
        self.headers = {"User-Agent": user_agent,
                        "Accept-Encoding": "gzip",
                        "Referer": "https://www.google.com"}

    def getWebContent(self, url):
        time_sleep = self.config.time_sleep
        if time_sleep > 0:
            time_sleep = time_sleep * random.random()
            print('time sleep: ' + str(time_sleep))
            time.sleep(time_sleep)

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

    def save(self, url, name):
        if url not in self._downloaded_photos:
            self._downloaded_photos.append(url)
            request.urlretrieve(url, name)
            print(url)

    def __makeDownloadDir(self):
        subclass_name = self.__class__.__name__
        sub_folder = os.path.join(
            self.config.download_path, 'photos', subclass_name)
        print(sub_folder)
        if not os.path.exists(sub_folder):
            os.mkdir(sub_folder)

        os.chdir(sub_folder)

    def getPhoto(self):
        self.__makeDownloadDir()
        start = 1
        for i in range(start, self.config.last_page):
            url = self.config.page_url + str(i)
            # time.sleep(1)
            self.download(url)
