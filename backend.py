import requests, os, csv, sys, re
import bs4
from requests.packages.urllib3.util.retry import Retry

###########################################################################
# BACKEND (LOGIC) CODE AREA

def get_seller(ebay_user):
    """ Gets the html page of the ebay_seller's (200) sold items. 
    Checks if the seller exists (whether results is greater than 0).
    If yes: prints title and results found; else: 'no results found'. """
    global soup
    url_start = 'https://www.ebay.co.uk/sch/m.html?_nkw=&_armrs=1&_from=&LH_Complete=1&LH_Sold=1&_ssn='
    url_sold_listings = '&_ipg=50&rt=nc' # first page 
    # construct a way to iterate through pages and collect all items in them
    # url extension: &_pgn=2&_skc=200&rt=nc
    full_url_link = url_start + ebay_user + url_sold_listings
    res = requests.get(full_url_link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # test whether any results has been returned
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
    """ Collects sellers listed, sold items with details of title, price, url. """
    # NOTE: find a logic way to create a dictionary in the following order:
    # dict = key: title, value: price, url
    for title, item, link in zip(soup.select('.vip'), soup.select('.bold.bidsold'), soup.select('.vip')):
        listing_dict.setdefault(title.text, []).append(item.get_text().strip())
        listing_dict.setdefault(title.text, []).append(link.get('href'))


##########################################
# TESTING AREA 
# def get_detailed_information(num_retries= 10):
#     """ Takes the listing url from the listing_dict and collects available detailed item information ()
#     from the page. """
#     counter = 0

#     # getting the soup 
#     soup = get_soup(url,num_retries)
#     print(counter)

#     # product_dict = {
#     #     'Title': get_title(soup),
#     # }
#     return soup.title()


# def get_soup(num_retries= 10):
#         s = requests.Session()

#         retries = Retry(
#             total = num_retries,
#             backoff_factor = 0.1,
#             status_forcelist = [500, 502, 503, 504]
#             )
#         print('happening')
#         return BeautifulSoup(s.get(url).text, 'lxml')


#         for value in ld.values():
#             r = requests.get(value[1])
#             soup = bs4.BeautifulSoup(r.text, 'lxml')
#             counter = 0
#             print('Loops: ', counter)


# ##########################################
# # TESTING AREA ENDS 

# ebay_user = 'rtwdirectsales'
# get_seller(ebay_user)
# seller_listed_items()
# get_detailed_information()
