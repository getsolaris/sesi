#-*-coding: utf-8 -*-

import re
import feedparser

VERSION = '0.0.2'
RSS_URL = 'http://blog.rss.naver.com/saskinio'

versions = []

def crawl():
    content = feedparser.parse(RSS_URL)

    for feed in content.entries:
        if feed.category == '릴리즈':
            versions.append([re.sub('[^0-9.]', '', feed.title).strip(), feed.link])

    return VERSION == versions[0][0]

if __name__ == "__main__":
    print(crawl())
    print(versions[0][1])