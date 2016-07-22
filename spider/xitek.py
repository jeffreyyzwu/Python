#-*-coding=utf-8-*-
__author__ = 'jeffrey'
from baseSpider import baseSpider, config
from bs4 import BeautifulSoup
import re
from urllib import request


class xitek(baseSpider):

    def __init__(self):
        super().__init__()
        cfg = config()
        self.config = cfg
        cfg.site_url = "http://photo.xitek.com/"
        cfg.page_url = "http://photo.xitek.com/style/0/p/"
        cfg.download_path = "photos"
        cfg.last_page = self.__get_last_page()

    def __get_last_page(self):
        bs = self.getBS4WebContent(self.config.site_url)
        page = bs.find_all('a', class_="blast")
        last_page = page[0]['href'].split('/')[-1]
        return int(last_page)

    def download(self, url):
        p = re.compile(r'href="(/photoid/\d+)"')
        html = self.getWebContent(url)
        content = p.findall(html)
        for i in content:
            bs = self.getBS4WebContent(self.config.site_url + i)
            final_link = bs.find('img', class_="mimg")['src']
            print(final_link)
            title = bs.title.string.strip()
            filename = re.sub('[\/:*?"<>|]', '-', title) + '.jpg'
            request.urlretrieve(final_link, filename)
