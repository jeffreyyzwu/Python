#-*-coding=utf-8-*-
__author__ = ''
from bs4 import BeautifulSoup
from urllib import request
import sys
import gzip
import time
import random
import re
import os
import importlib

importlib.reload(sys)


class Xitek():

    def __init__(self):
        self.url = "http://photo.xitek.com/"
        user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers = {"User-Agent": user_agent,
                        "Referer": "https://www.google.com"}
        self.last_page = self.__get_last_page()

    def __get_last_page(self):
        html = self.__getContentAuto(self.url)
        bs = BeautifulSoup(html, "html.parser")
        page = bs.find_all('a', class_="blast")
        last_page = page[0]['href'].split('/')[-1]
        return int(last_page)

    def __getContentAuto(self, url):
        req = request.Request(url, headers=self.headers)
        res = request.urlopen(req)
        # time.sleep(2*random.random())
        charset = res.headers.get_content_charset()
        content = res.read()
        info = res.info().get("Content-Encoding")
        if info == None:
            return content.decode(charset)
        else:
            html = gzip.decompress(content).decode(charset)
            return html

    def __download(self, url):
        p = re.compile(r'href="(/photoid/\d+)"')
        html = self.__getContentAuto(url)
        content = p.findall(html)
        for i in content:
            photoid = self.__getContentAuto(self.url + i)
            bs = BeautifulSoup(photoid, "html.parser")
            final_link = bs.find('img', class_="mimg")['src']
            print(final_link)
            title = bs.title.string.strip()
            filename = re.sub('[\/:*?"<>|]', '-', title) + '.jpg'
            request.urlretrieve(final_link, filename)

    def getPhoto(self):
        start = 0
        photo_url = "http://photo.xitek.com/style/0/p/"
        for i in range(start, 1):  # self.last_page + 1):
            url = photo_url + str(i)
            # time.sleep(1)
            self.__download(url)


def main():
    sub_folder = os.path.join(os.getcwd(), "content")
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    os.chdir(sub_folder)
    obj = Xitek()
    obj.getPhoto()


if __name__ == "__main__":
    main()
