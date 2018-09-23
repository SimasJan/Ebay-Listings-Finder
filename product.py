import requests, os, csv, sys, re
import bs4
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import unicodedata

#url = "https://www.ebay.co.uk/itm/Digital-Pocket-Mini-Weighing-Scales-for-Gold-Jewellery-Herbs-Silver-Scrap-350g/111810440300?hash=item1a086bec6c:g:H8wAAOSw5VFWM4QM"
#url = "https://www.ebay.co.uk/itm/Braun-CRZ5BH-Cruzer5-Mens-Rechargeable-Corded-Cordless-Beard-Trimmer-Clipper-New/192162277164?_trkparms=aid%3D777001%26algo%3DDISCO.FEED%26ao%3D1%26asc%3D20160801204525%26meid%3Df308dd4d9f134592948858a69f0133c1%26pid%3D100651%26rk%3D1%26rkt%3D1%26%26itm%3D192162277164&_trksid=p2481888.c100651.m4497&_trkparms=pageci%3A239cbbeb-bf3b-11e8-aeb1-74dbd180d4e1%7Cparentrq%3A06c91d7f1660ab4cdd4b68b6fffba728%7Ciid%3A1"
#url = "https://www.ebay.co.uk/itm/100X-Jewelry-Microscope-LED-Light-Magnifying-Magnifier-Jeweler-Loupe-Eye-Coins/302589690613?_trkparms=aid%3D333200%26algo%3DCOMP.MBE%26ao%3D1%26asc%3D20180409081753%26meid%3Dce3800a11346454bb6909945ec4ee103%26pid%3D100008%26rk%3D2%26rkt%3D12%26sd%3D111810440300%26itm%3D302589690613&_trksid=p2047675.c100008.m2219"
#url = "https://www.ebay.co.uk/itm/JBL-90W-2-WAY-4-INCH-10cm-CAR-VAN-DOOR-SHELF-COAXIAL-SPEAKERS-GRILLS-NEW-PAIR/191831447320?hash=item2caa0b9718:g:hGkAAOSwu1VW7s-B%27"
#url = "https://www.ebay.co.uk/itm/NEW-Square-Folding-Standard-Bridge-Card-Game-Black-Table/172834224891?hash=item283db8fafb:g:8CwAAOSwUMxZ80~i"
#url = "https://www.ebay.co.uk/itm/NEW-Professional-Knee-Kicker-Stretcher-Carpet-Fitters-Gripper-Tool-Green/172723981120?hash=item283726cb40:g:J6kAAOSwALtafYQJ"

urls = [
    'https://www.ebay.co.uk/itm/Digital-Pocket-Mini-Weighing-Scales-for-Gold-Jewellery-Herbs-Silver-Scrap-350g/111810440300?hash=item1a086bec6c:g:H8wAAOSw5VFWM4QM',
    'https://www.ebay.co.uk/itm/Braun-CRZ5BH-Cruzer5-Mens-Rechargeable-Corded-Cordless-Beard-Trimmer-Clipper-New/192162277164?_trkparms=aid%3D777001%26algo%3DDISCO.FEED%26ao%3D1%26asc%3D20160801204525%26meid%3Df308dd4d9f134592948858a69f0133c1%26pid%3D100651%26rk%3D1%26rkt%3D1%26%26itm%3D192162277164&_trksid=p2481888.c100651.m4497&_trkparms=pageci%3A239cbbeb-bf3b-11e8-aeb1-74dbd180d4e1%7Cparentrq%3A06c91d7f1660ab4cdd4b68b6fffba728%7Ciid%3A1',
    'https://www.ebay.co.uk/itm/100X-Jewelry-Microscope-LED-Light-Magnifying-Magnifier-Jeweler-Loupe-Eye-Coins/302589690613?_trkparms=aid%3D333200%26algo%3DCOMP.MBE%26ao%3D1%26asc%3D20180409081753%26meid%3Dce3800a11346454bb6909945ec4ee103%26pid%3D100008%26rk%3D2%26rkt%3D12%26sd%3D111810440300%26itm%3D302589690613&_trksid=p2047675.c100008.m2219',
]

def get_all_products(url, num_retries=10):
    global soup
    global product_dict
    soup = get_soup(url, num_retries=10)

    product_dict = {
        'Title': get_title(soup),
        'Sub-title': get_subtitle(soup),
        'Condition': get_condition(soup),
        'Price': get_price(soup),
        'Qnty': get_quantity(soup),
        'Units Sold': units_sold(soup),
        'Location': get_location(soup),
        'Returns': get_returns_policy(soup),
        'Specifics': get_specifics(soup),
    }
    return product_dict

def get_soup(url, num_retries =10):
    s = requests.Session()

    retries = Retry(
        total = num_retries,
        backoff_factor = 0.1,
        status_forcelist = [500, 502, 503, 504]
        )
    
    s.mount('http://', HTTPAdapter(max_retries = retries))

    # for url in urls:
    #     return bs4.BeautifulSoup(s.get(url).text, 'lxml')
    return bs4.BeautifulSoup(s.get(url).text, 'lxml')

def get_title(soup):
    print('Title: ', soup.title.string.split('|')[0])
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

# def get_item_specific(soup):
#     item_specifics = {}
#     k = []
#     v = []
#     for item in soup.find_all('div', {'class':'section'}):
#         for td, value in zip(item.select('td.attrLabels'), item.select('td > span')):
#             item_specifics.setdefault(td.get_text(strip=True), []).append(value.get_text(strip=True))
#             k.append(td.get_text(strip=True))
#             v.append(value.get_text(strip=True))

#     #return (k,v)
#     # for key, value in zip(k, v):
#     #     item_specifics[key] = value

#     return item_specifics

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

allProductList = []

def megaList():
    for url in urls:
        allProductList.append(get_all_products(url))
        print("Total items returned: ", len(allProductList))
        #print(allProductList)
    
    # for item in allProductList:
    #     print(allProductList)
    #     print('-'*50)

    # return allProductList


megaList()

# print('-'*15)
# print('PRINTED VERSION:\n',allProductList)
# print('-'*15)