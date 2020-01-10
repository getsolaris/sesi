import re
import feedparser

VERSIONS = []
RSS_URL = 'http://blog.rss.naver.com/saskinio'

def release_rss_crawl(version):
    content = feedparser.parse(RSS_URL)

    for feed in content.entries:
        if feed.category == '릴리즈':
            VERSIONS.append([re.sub('[^0-9.]', '', feed.title).strip(), feed.link])
            break

    return [version == VERSIONS[0][0], VERSIONS]