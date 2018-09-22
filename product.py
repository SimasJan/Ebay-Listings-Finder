import requests, os, csv, sys, re
import bs4
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import unicodedata

url = "https://www.ebay.co.uk/itm/Digital-Pocket-Mini-Weighing-Scales-for-Gold-Jewellery-Herbs-Silver-Scrap-350g/111810440300?hash=item1a086bec6c:g:H8wAAOSw5VFWM4QM"

def get_all_products(url):
    global soup
    global product_dict
    soup = get_soup()

    product_dict = {
        'Title': get_title(soup),
        'Sub-title': get_subtitle(soup),
        'Condition': get_condition(soup),
        'Price': get_price(soup),
        'Qnty': get_quantity(soup),
        'Units Sold': units_sold(soup),
        'Location': get_location(soup),
        'Returns': get_returns_policy(soup),
        'EAN': get_ean(soup),
    }
    return product_dict

def get_soup(num_retries =10):
    s = requests.Session()

    retries = Retry(
        total = num_retries,
        backoff_factor = 0.1,
        status_forcelist = [500, 502, 503, 504]
        )
    
    s.mount('http://', HTTPAdapter(max_retries = retries))

    # urls = []
    # for value in ld.values():
    #     urls.append(value[1])
    # print('{} urls added.'.format(len(urls)))

    return bs4.BeautifulSoup(s.get(url).text, 'lxml')

def get_title(soup):
    #print('Title: ', soup.title.string.split('|')[0])
    return soup.title.string.split('|')[0]

def get_subtitle(soup):
    for value in soup.select('#subTitle'):
        subtitle = value.get_text(strip=True)
    if not subtitle:
        return 'N/A'
    elif subtitle:
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
    for item in soup.select('.vi-qtyS-hot-red'):
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

def get_item_specifics():
    item_specific = {
    }
    specific_name = []
    specific_value = []

    for item in soup.find_all('div', {'class':'itemAttr'}):
        for td in item.select('td.attrLabels'):
            specific_name.append(td.get_text(strip=True))

            #item_specific.setdefault(td.get_text(strip=True), [])

    for value in soup.find_all('div', {'class':'itemAttr'}):
        for td in value.select('td > span'):
            specific_value.append(td.get_text(strip=True))


    return specific_name, specific_value



get_all_products(url)

print('-'*15)
print('PRINTED VERSION:\n',product_dict)
print('-'*15)