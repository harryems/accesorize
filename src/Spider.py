import cookielib
import csv
import os
import re
import socket
import urllib
import urllib2
import time
from bs4 import BeautifulSoup
#from utils.Csv import Csv

__author__ = 'Carlos Espinosa'

import threading

class Downloader(threading.Thread):
    def __init__(self, url, downloadPath):
        threading.Thread.__init__(self)
        self.url = url
        self.downloadPath = downloadPath

    def run(self):
        self.downloadFile(self.url, self.downloadPath)

    def downloadFile(self, url, downloadPath):
        print "image URL" + url
        try:
            socket.setdefaulttimeout(10)
            opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0))
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1')]
            urllib2.install_opener(opener)
            response = None
            try:
                response = opener.open(url, timeout=30)
            except Exception, x:
                print x
            if response is None: return False

#            print response.info()
            contentLength = response.info()['Content-Length']
            lengthChunk = re.search('(?i)^(\d+)', contentLength)
            if lengthChunk:
                contentLength = lengthChunk.group(1)
            else:
                contentLength = 0
            totalSize = float(contentLength)
            directory = os.path.dirname(downloadPath)
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except Exception, x:
                    print x
            dl_file = open(downloadPath, 'wb')
            currentSize = 0
            CHUNK_SIZE = 32768
            totalSizeKB = totalSize / 1024 if totalSize > 0 else totalSize
            while True:
                data = None
                try:
                    data = response.read(CHUNK_SIZE)
                except Exception, x:
                    print x
                if not data:
                    break
                currentSize += len(data)
                dl_file.write(data)

                notifyDl = '===> Downloaded ' + str(round(float(currentSize * 100) / totalSize, 2)) + '% of ' + str(
                    totalSizeKB) + ' KB.'
                #print notifyDl

                if currentSize >= totalSize:
                    dl_file.close()
                    return True
        except urllib2.HTTPError as x:
            error = 'Error downloading: ' + x
            print error
        except Exception, x:
            error = 'Error downloading: ' + x
            print error
            return False


class Spider:
    def __init__(self):
        self.opener = None
        self.RETRY_COUNT = 5
        self.USER_AGENT = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        self.headers = [self.USER_AGENT]


    def fetchData(self, url, referer=None, parameters=None, retry=0):
        """
        Fetch data from a url
        url='' Ex. http://www.example.com, https://www.example.com
        parameters={} Ex. {'user': 'user', 'pass': 'pass'}
        """
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
                                      urllib2.HTTPHandler(debuglevel=0),
                                      urllib2.HTTPSHandler(debuglevel=0))


        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1'),
                             ('Referer', 'http://us.accessorize.com')]
        cookieJar = cookielib.LWPCookieJar()
        handlers = urllib2.HTTPCookieProcessor(cookieJar)

        opener.add_handler(handlers)


        urllib2.install_opener(opener)
        response = opener.open(url)
        return response.info(), response.read()
        
        self.REFERER = ('Referer', referer)
        if referer is not None:
            self.headers.append(self.REFERER)
        self.opener = self.createOpener(self.headers, [self.createCookieJarHandler()])
        urllib2.install_opener(self.opener)
        try:
            if parameters is None:
                response = self.opener.open(url, timeout=30)
                return response.info(), response.read()
            else:
                response = self.opener.open(url, urllib.urlencode(parameters), timeout=30)
                return response.info(), response.read()
        except Exception, x:
            print x
            if retry < self.RETRY_COUNT:
                self.fetchData(url, referer, parameters, retry + 1)
            else:
                print 'Failed to fetch data after 5 retry.'
        return None


#    def createOpener(self, headers=None, handlers=None):
#        """
#        Create opener for fetching data.
#        headers = [] Ex. User-agent etc like, [('User-Agent', HEADERS), ....]
#        handler = object Ex. Handler like cookie_jar, auth handler etc.
#        return opener
#        """
#        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
#            urllib2.HTTPHandler(debuglevel=0),
#            urllib2.HTTPSHandler(debuglevel=0))
#        if headers is not None:
#            opener.addheaders = headers
#        if handlers is not None:
#            for handler in handlers:
#                opener.add_handler(handler)
#        return opener

#   def createCookieJarHandler(self):
#        """
#        Create cookie jar handler. used when keep cookie at login.
#        """
#        cookieJar = cookielib.LWPCookieJar()
#        return urllib2.HTTPCookieProcessor(cookieJar)


class Main:
    def __init__(self, url, csvFile):
        self.spider = Spider()
        self.mainUrl = url
        self.referer = None
        self.archive = csv.writer(open(csvFile, 'ab'))
        self.bulk=open("bulk.txt", "w")

    def doOperation(self):
        if self.referer is None:
            headerInfo, data = self.spider.fetchData(self.mainUrl)
            if headerInfo is not None:
                responseCookie = headerInfo['Set-Cookie']
                lastDomainCookie = re.search('(?i)lastDomainCookie=([a-zA-Z0-9.]+);', responseCookie)
                if lastDomainCookie:
                    self.referer = 'http://' + str(lastDomainCookie.group(1))

        self.scrapData(self.mainUrl, self.referer)

    def scrapData(self, url, referer):
        headerInfo, data = self.spider.fetchData(url, referer)

        mainPageSoup = BeautifulSoup(data)

        menu = mainPageSoup.find("div", {"class": "mainNavigation_linkList_content"})
        #print(menu)
        for menuSegundoNivel in menu.find_all("div", {"class": "secondLevelNavOnwards"}):
            for hrefCategory in menuSegundoNivel.find_all('a'):
                hrefCategory = hrefCategory.get('href')
                if hrefCategory is not None and len(hrefCategory) > 0:
                    categoryUrl = self.mainUrl + hrefCategory
                    self.scrapCategoryData(categoryUrl)

    def scrapCategoryData(self, url, page=1):
        categoryUrl = url + '?pageSize=500&showAll=true&sort=score&page=' + str(page) ## &showAll=true
        print 'Category URL: ' + categoryUrl
        try:
            headerInfo, categoryPageRequest = self.spider.fetchData(categoryUrl, self.referer)
            categoryPagesoup = BeautifulSoup(categoryPageRequest)
            hrefItems = categoryPagesoup.find_all('div', {"class": "productList_name"})
            if hrefItems and len(hrefItems) > 0:
                print 'Total Items Found: ' + str(len(hrefItems))
                for hrefItem in hrefItems:
                    hrefItem = hrefItem.find('a').get('href')
                    if hrefItem is not None and len(hrefItem) > 0:
                        itemUrl = self.mainUrl + hrefItem
                        self.scrapItem(itemUrl)

            if categoryPageRequest is not None and len(categoryPageRequest) > 0:
                data = re.sub('(?i)\n+', ' ', categoryPageRequest)
                data = re.sub('(?i)\s+', ' ', data)
                if re.search('<a href="[^"]*" class="pagination_next">', data):
                    return self.scrapCategoryData(url, page + 1)
        except Exception, x:
            print x

    def scrapItem(self, url):
        #print 'Item URL: ' + url
        try:
            headerInfo, itemPageRequest = self.spider.fetchData(url, self.referer)
            itemPagesoup = BeautifulSoup(itemPageRequest)
            code = itemPagesoup.find("p", {"class": "productCode"}).string
            image = itemPagesoup.find("div", {"class": "ql_product_picture floatProperties"}).find(
                'a').get('href')
            description = itemPagesoup.find("div", {"class": "productDescriptionText"}).string.strip()
            downloader = Downloader(image, 'C:/Users/Carlos/workspace/accessorize/src/media/' + str(code) + ".jpg")
            downloader.start()
            ahora=time.strftime('%Y-%m-%d %H:%M:%S')
            sql=",1,\""+ahora+"\",\""+ahora+"\", , "+str(code)+" ,,inherit,open,open,,"+str(code)+",,,\" "+ahora+"\",\"" +ahora+ "\" ,,,http://127.0.0.1/accesorize/wp-content/uploads/"+ str(code) + ".jpg,0,attachment,image/jpeg,0 "                       
            self.bulk.writelines(sql)
            #print(row)
            #self.archive.writerow(row)
            #archive.writerow(row)
        except Exception, x:
            print x


if __name__ == "__main__":
    country = "uk"
    mainUrl = "http://" + country + ".accessorize.com"
    main = Main(mainUrl, 'test.csv')
    main.doOperation()