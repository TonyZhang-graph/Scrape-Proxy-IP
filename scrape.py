# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import csv
import time
import random

CRAWLPAGELIMIT = 100 # crawl from page1 to CRAWLPAGELIMIT
CRAWLTIMESPAN = 1 # number of seconds between two request

class ProxyIP:
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
    def getPage(self, url, userAgent):
        request = Request(url)
        request.add_header('User-agent', userAgent)
        html = urlopen(request)
        bs = BeautifulSoup(html.read(),'html.parser')
        return bs
    
    def safeGet(self, bs, selector):
        try:
            result = bs.select(selector)
        except AttributeError:
            print('Some attributes are missing.')
        return result
    
    def parse(self, bs, website):
        ipList = self.safeGet(bs, website.ipTag)
        portList = self.safeGet(bs, website.portTag)
        locationList = self.safeGet(bs, website.locationTag)
        respondTimeList = self.safeGet(bs, website.respondTimeTag)
        proxyIps = []
        for ip, port, location, respondTime in zip(ipList, portList, locationList, respondTimeList):
            proxyIp = ProxyIP(ip.get_text(), port.get_text(), location.get_text(), respondTime.get_text())
            proxyIps.append(proxyIp)
        return proxyIps
        
    def crawl(self, website, writer, userAgent):
        bs = self.getPage(website.url, userAgent)
        proxyIps = self.parse(bs, website)
        for proxyIp in proxyIps:
            writer.writerow([proxyIp.ip, proxyIp.port, proxyIp.location, proxyIp.respondTime])
   
    
userAgents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
]
     
outFile = open('ipData.csv', 'w', newline = '')
writer = csv.writer(outFile)
crawler = Crawler()
websiteDatas = [
        ['https://www.kuaidaili.com/free/inha/{0}/'.format(page),'td[data-title="IP"]', 'td[data-title="PORT"]', 'td[data-title="位置"]', 'td[data-title="响应速度"]']
        for page in range(1, CRAWLPAGELIMIT + 1)
]
websites = []

for websiteData in websiteDatas:
    website = Website(websiteData[0], websiteData[1], websiteData[2], websiteData[3], websiteData[4])
    websites.append(website)
    
for website in websites:
    print('Crawling in: {}'.format(website.url))
    crawler.crawl(website, writer, userAgents[random.randint(0, len(userAgents) - 1)])
    time.sleep(CRAWLTIMESPAN)
print('Finished')
    
outFile.close()
