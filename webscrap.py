from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import os


st = raw_input("Search: ")
pg = int(raw_input("Pages: "))

dr = os.getcwd()
filename = dr + "\\" + st + " products.csv"
f = open(filename, "w")
headers = "Brand, Model, Price, MarketPlace\n"
site = 'http://www.bestbuy.com'

f.write(headers)

cp = 1
for i in xrange(pg):
    my_url = 'http://www.bestbuy.com/site/searchpage.jsp?cp=' + str(cp) + '&searchType=search&st=' + str(st.replace(" ", "%20")) + '&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys'

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.find_all("div", {"class":"list-item"})

# print containers[0]['data-name']
# print containers[0].h4.a.getText()

    for container in containers:

        brand = container.h4.a.text.split(',')[0].encode('utf-8')
        print brand
        model = container.find("span", {"class": "sku-value"}).text
        print model
        d = json.loads(container['data-price-json'])
        price = d.get('currentPrice')
        if price is None:
            price = (d.get('priceDomain')).get('currentPrice')
        print price
        link = container.h4.a['href']
        marketplace = str(site + link)

        f.write(brand + "," + model.encode('utf-8') + "," + str(price) + "," + marketplace + "\n")

    cp += 1