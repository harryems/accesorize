import cookielib
import csv
import re
import socket
import urllib
import urllib2
from bs4 import BeautifulSoup
import xmlrpclib
import threading

__author__ = 'Carlos Espinosa'

class InsertItems(threading.Thread):
    def __init__(self,code,description,idImage):
        threading.Thread.__init__(self)
        self.code = code
        self.description = description
        self.idImage=idImage
    def run(self):
        self.insertItem(self.code,self.description,self.idImage)

        

class Downloader(threading.Thread):
    def __init__(self, url,code,description):
        threading.Thread.__init__(self)
        self.url = url
        self.code = code
        self.description=description

    def run(self):
        self.downloadFile(self.url,self.code,self.description)

    def downloadFile(self, url,code,description):
        try:
            wp_url = "http://127.0.0.1/accesorize/xmlrpc.php"
            wp_username = "carlos.espinosa"
            wp_password = "@#5M0k137"
            wp_blogid = ""            
            socket.setdefaulttimeout(20)
            file_url = url.split("?")
            file_url = file_url[0]
            extension = file_url.split(".")
            leng = extension.__len__()
            extension = extension[leng-1]            
            if (extension=='jpg'):
                xfileType = 'image/jpeg'
            elif(extension=='png'):
                xfileType='image/png'
            elif(extension=='bmp'):
                xfileType = 'image/bmp'
            file = xmlrpclib.Binary(urllib2.urlopen(file_url).read())
            server = xmlrpclib.Server(wp_url)
            mediarray = {'name':code+'.'+extension, 
                         'type':xfileType, 
                         'bits':file 
                         }
            insertImage = [wp_blogid,wp_username,wp_password , mediarray]
            result = server.wp.uploadFile(insertImage)
            idImage= result['id']
            self.insertItem(code,description,idImage)
        except urllib2.HTTPError as x:
            pass
            #error = 'Error downloading: ' + x
            #print error
        except Exception, x:
            #error = 'Error downloading: ' + x
            #print error
            return False
    def insertItem(self,code,description,idImage):
        try:
            print idImage + "," +code+ "," +description
            
            wp_url = "http://127.0.0.1/accesorize/xmlrpc.php"
            wp_username = "carlos.espinosa"
            wp_password = "@#5M0k137"
            wp_blogid = ""
            server = xmlrpclib.ServerProxy(wp_url)
            metas = [
                        {'key': 'regular_price','value':''},
                        {'key': 'sale_price','value':''},
                        {'key': 'weight','value':'0'},
                        {'key': 'length','value':'0'},
                        {'key': 'width','value':'0'},
                        {'key': 'height','value':'0'},
                        {'key': 'tax_status','value':'taxable'},
                        {'key': 'tax_classes','value':'a:1:{i:0;s:1:"*";}'},
                        {'key': 'visibility','value':'visible'},
                        {'key': 'featured','value':''},
                        {'key': 'customizable','value':'no'},
                        {'key': 'customized_length','value':''},
                        {'key': 'product_attributes','value':''},
                        {'key': 'manage_stock','value':''},
                        {'key': 'stock_status','value':'instock'},
                        {'key': 'sale_price_dates_from','value':''},
                        {'key': 'sale_price_dates_to','value':''}
                     ]
            data = {'post_title': str(code), 'post_content':description,'post_type':'product', 'post_status':'publish' ,'post_thumbnail':idImage, 'custom_fields':metas }
            tri=server.wp.newPost(wp_blogid, wp_username, wp_password, data)
            print tri
        except urllib2.HTTPError as x:
            #pass
            error = 'Error downloading: ' + str(x)
            print error
        except Exception, x:
            error = 'Error downloading: ' + str(x)
            print error
            return False


class Spider:
    def __init__(self):
        self.opener = None
        self.RETRY_COUNT = 5
        self.USER_AGENT = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        self.headers = [self.USER_AGENT]


    def fetchData(self, url, referer=None, parameters=None, retry=0):
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
        try:
            headerInfo, itemPageRequest = self.spider.fetchData(url, self.referer)
            itemPagesoup = BeautifulSoup(itemPageRequest)
            code = itemPagesoup.find("p", {"class": "productCode"}).string
            image = itemPagesoup.find("div", {"class": "ql_product_picture floatProperties"}).find(
                'a').get('href')
            description = itemPagesoup.find("div", {"class": "productDescriptionText"}).string.strip()
            #row = [code, description, image]
            downloader = Downloader(image,code,description)
            downloader.start()
            #insert = InsertItems(code,description,idImage)
            #insert.start()
            
            #ahora=time.strftime('%Y-%m-%d %H:%M:%S')
            #sql=",1,\""+ahora+"\",\""+ahora+"\", , "+str(code)+" ,,inherit,open,open,,"+str(code)+",,,\" "+ahora+"\",\"" +ahora+ "\" ,,,http://127.0.0.1/accesorize/wp-content/uploads/"+ str(code) + ".jpg,0,attachment,image/jpeg,0 "                       
            #self.bulk.writelines(sql)
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