import requests, os, csv, sys, re
import bs4
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import unicodedata

###########################################################################
# BACKEND (LOGIC) CODE AREA

def get_seller(ebay_user):
    """ Gets the html page of the ebay_seller's (200) sold items. 
    Checks if the seller exists (whether results is greater than 0).
    If yes: prints title and results found; else: 'no results found'. """
    global soup
    url_start = 'https://www.ebay.co.uk/sch/m.html?_nkw=&_armrs=1&_from=&LH_Complete=1&LH_Sold=1&_ssn='
    url_sold_listings = '&_ipg=20&rt=nc'
    full_url_link = url_start + ebay_user + url_sold_listings
    res = requests.get(full_url_link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    for item in soup.find_all('span', {'class':'rcnt'}):
        if str(item.get_text()) == str(0):
            print('-'*30)
            return 'no results found. Please check your name.'
            break
        elif str(item.get_text()) > str(0):
            for title in soup.select('title'):
                print('-'*30)
                print('Seller Found: {} | Results: {}'.format(title.get_text(), item.get_text()))
        else:
            print('-'*30)
            print('Something gone wrong...')
            break

listing_dict = {}

def seller_listed_items():
    print('Collecting sold listings....')
    print('-'*55)
    """ Collects sellers listed, sold items with details of title, price, url. """
    # NOTE: find a logic way to create a dictionary in the following order:
    # dict = key: title, value: price, url
    for title, item, link in zip(soup.select('.vip'), soup.select('.bold.bidsold'), soup.select('.vip')):
        listing_dict.setdefault(title.text, []).append(item.get_text().strip())
        listing_dict.setdefault(title.text, []).append(link.get('href'))
        print('total items added {}'.format(len(listing_dict)))

def get_all_products(url, num_retries=10):
    print('collecting detailed product information....')
    print('-'*55)

    global soup
    global product_dict
    soup = get_soup(url, num_retries=10)

    product_dict = {
        'Title': get_title(soup),
        'Specifics': get_specifics(soup),
    #     'Sub-title': get_subtitle(soup),
    #     'Condition': get_condition(soup),
    #     'Price': get_price(soup),
    #     'Qnty': get_quantity(soup),
    #     'Units Sold': units_sold(soup),
    #     'Location': get_location(soup),
    #     'Returns': get_returns_policy(soup),
        'link': get_url_link(soup),
    }
    return product_dict

def get_soup(url,num_retries =10):
    s = requests.Session()

    retries = Retry(
        total = num_retries,
        backoff_factor = 0.1,
        status_forcelist = [500, 502, 503, 504]
        )
    
    s.mount('http://', HTTPAdapter(max_retries = retries))
    # print('URL INSERTED IN GET SOUP:\n',url)
    return bs4.BeautifulSoup(s.get(url).text, 'lxml')

def get_title(soup):
    print(soup.title.string.split('|')[0],'-'*10)
    return soup.title.string.split('|')[0]

def get_subtitle(soup):
    for value in soup.select('#subTitle'):
        if value == None:
            subtitle = 'N/A'
        else:
            subtitle = value.get_text(strip=True)
    
        if not subtitle:
            return 'N/A'
        else:
            return subtitle

def get_condition(soup):
    for value in soup.select('#vi-itm-cond'):
        condition = value.get_text(strip=True)
    
    if not condition:
        return 'N/A'
    elif condition:
        return condition

def get_price(soup):
    for text in soup.select('#prcIsum'):
        price = text.get_text()

    if not price:
        return 'N/A'
    elif price:
        return price

def get_quantity(soup):
    for item in soup.select('#qtySubTxt > span'):
        quantity = item.get_text(strip=True)

    if not quantity:
        return 'N/A'
    
    if quantity == 'More than 10 available':
        return '>10'
    elif quantity == 'Limited quantity available':
        return 'Limited Qnty'
    elif quantity == 'Last one':
        return '1'
    else:
        return quantity[:-10]

def units_sold(soup):
    for item in soup.find_all('span', {'class': ['vi-qtyS-hot-red', 'vi-qtyS']}):
        units_sold = item.get_text(strip=True)

    if not units_sold:
        return 'N/A'
    else:
        return units_sold

def get_location(soup):
    for span in soup.select('div.iti-eu-bld-gry > span'):
        return span.contents[0]
    
    
def get_returns_policy(soup):
    for value in soup.select('#vi-ret-accrd-txt'):
        return_policy = value.get_text()
    
    return_policy = unicodedata.normalize("NFKD", return_policy)
    
    if not return_policy:
        return 'N/A'
    elif return_policy:
        return return_policy

def get_specifics(soup):
    k = []
    v = []
    for item in soup.find_all('div', {'class':'section'}):
        for td in item.select('td.attrLabels'):
            k.append(td.get_text(strip=True))
        for value in item.select('td > span'):
            v.append(value.get_text(strip=True))

    item_specifics = {}
    for k,v in zip(k[1:],v):
        item_specifics[k] = v

    return item_specifics

def get_url_link(soup):
    for value in listing_dict.values():
        return value[1]

allProductList = []

def megaList():
    print('-'*50)
    print('collecting detailed product information....')
    print('-'*50)

    for value in listing_dict.values():
        allProductList.append(get_all_products(value[1]))
        print('-'*10)
        print("Total items returned: ", len(allProductList))
        print('-'*10)


# ebay_user = 'rtwdirectsales'
# get_seller(ebay_user)
# seller_listed_items()

# megaList()

# print(allProductList)