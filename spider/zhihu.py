#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'jeffrey'

from baseSpider import baseSpider, config
from bs4 import BeautifulSoup
import re


class zhihu(baseSpider):

    def __init__(self):
        super().__init__()
        cfg = config()
        self.config = cfg
        cfg.site_url = "https://www.zhihu.com"
        cfg.page_url = ""
        cfg.last_page = 2
        cfg.time_sleep = 2

    def __imageTag(self, tag):
        return tag.name == 'img' and tag.has_attr(r"data-actualsrc")

    def download(self, url):
        p = re.compile(r'href="(/question/\d+)"')
        html = self.getWebContent(url)
        content = p.findall(html)
        for questionurl in content:
            qurl = self.config.site_url + questionurl
            self.__downloadPhotos(qurl)

    def __downloadPhotos(self, url):
        p = re.compile(r"zhimg.com/(\w+.\w+)")  # 图片名正则
        bs = self.getBS4WebContent(url)
        images = bs.find_all(self.__imageTag)
        for image in images:
            link = image['data-actualsrc']
            filename, *_ = p.findall(link)
            self.save(link, filename)
