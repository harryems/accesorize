





class Main:
    def __init__(self, url):
        self.spider = Spider()
        self.mainUrl = url

    def doOperation(self):
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







url='http://uk.accessorize.com/uk/jewellery/rings'
cadena=url.split("/")
leng = cadena.__len__()
primer = cadena[leng-1] 
segunda = cadena[leng-2]

print "primera " + primer
print "segunda" + segunda
