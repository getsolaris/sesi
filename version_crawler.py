import re
import feedparser

RSS_URL = 'http://blog.rss.naver.com/saskinio'

def release_rss_crawl(version):
    versions = []
    content = feedparser.parse(RSS_URL)

    for feed in content.entries:
        if feed.category == '릴리즈':
            versions.append([re.sub('[^0-9.]', '', feed.title).strip(), feed.link])
            break

    return [version == versions[0][0], versions]

def version_content():
    releases = []
    content = feedparser.parse(RSS_URL)

    for feed in content.entries:
        if feed.category == '릴리즈':
            summary = feed.summary.replace('*', '\n')

            releases.append([
                re.sub('[^0-9.]', '', feed.title).strip(),
                summary
            ])

    return releases