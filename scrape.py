
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import time

class Content:
    """
    This class saves the content of one proxy ip.
    """
    def __init__(self, ip, port, location, respondTime):
        self.ip = ip
        self.port = port
        self.location = location
        self.respondTime = respondTime
        
    def __repr__(self):
        return 'IP: {0}, Port: {1}, Location: {2}, Respond Time: {3}'.format(self.ip, self.port, self.location, self.respondTime)
        
class Website:
    """
    This class saves the structure of one website
    """
    def __init__(self, url, ipTag, portTag, locationTag, respondTimeTag):
        self.url = url
        self.ipTag = ipTag
        self.portTag = portTag
        self.locationTag = locationTag
        self.respondTimeTag = respondTimeTag
        
class Crawler:
    def getPage(self, url):
        html = urlopen(url)
        bs = BeautifulSoup(html.read(),'html.parser')
        return bs
    
    def parse(self, bs, website):
        ipList = bs.select(website.ipTag)
        portList = bs.select(website.portTag)
        locationList = bs.select(website.locationTag)
        respondTimeList = bs.select(website.respondTimeTag)
        contents = []
        for ip, port, location, respondTime in zip(ipList, portList, locationList, respondTimeList):
            content = Content(ip.get_text(), port.get_text(), location.get_text(), respondTime.get_text())
            contents.append(content)
        return contents
        
    def crawl(self, website, writer):
        bs = self.getPage(website.url)
        contents = self.parse(bs, website)
        for content in contents:
            writer.writerow([content.ip, content.port, content.location, content.respondTime])
        
outFile = open('ipData.csv', 'w', newline = '')
writer = csv.writer(outFile)
crawler = Crawler()
websiteDatas = [
        ['https://www.kuaidaili.com/free/inha/{0}/'.format(page),'td[data-title="IP"]', 'td[data-title="PORT"]', 'td[data-title="位置"]', 'td[data-title="响应速度"]']
        for page in range(1, 20)
]
websites = []

for websiteData in websiteDatas:
    website = Website(websiteData[0], websiteData[1], websiteData[2], websiteData[3], websiteData[4])
    websites.append(website)
    
for website in websites:
    print('Scraping in page: {}'.format(website.url))
    crawler.crawl(website, writer)
    time.sleep(1)
    
outFile.close()
