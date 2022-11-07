import argparse
import requests 
from bs4 import BeautifulSoup
import json
import csv

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0

    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char 
    if 'sold' in text:
        return int(numbers)
    else:
        return 0 


def parse_shipping(text):
    '''
    Turn shipping cost into cents, stored as an integer; if the item has free shipping, then the value will be 0.
    
    >>> parse_shipping('+$7.49 shipping')
    749
    >>> parse_shipping('Free 3 day shipping')
    0
    >>> parse_shipping('Free shipping')
    0
    '''

    shipping = ''
    if text[0]== '+':
        for char in text:
            if char in '1234567890':
                shipping += char
        return int(shipping)
    elif 'free' in text.lower():
        shipping = 0
        return shipping



def parse_price(text):
    '''
    Contains the price of the item in cents, stored as an integer.

    >>> parse_price('$9.99')
    999
    >>> parse_price('$10.99')
    1099
    >>> parse_price('$123.44')
    12344

    '''
    
    numbers = ''
    if text[0]=='$':
        for char in text:
            if char in '1234567890':
                numbers += char 
        return int(numbers)
    else: 
        return None 


# this if statement says to only run the code below when the python file is run "normally"
# where normally means not in the doctests 

if __name__ == '__main__':


    # get command line arguments 
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default = 10)
    parser.add_argument('--csv', action = 'store_true')
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    #list of all items found in all ebay webpages 
    items = []

    #loop over the ebay pages
    for page_number in range(1,int(args.num_pages)+ 1):
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term
        url += '&_sacat=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url=', url)

    # download the html 
        r = requests.get(url)
        status = r.status_code
        print('status=', status )
        html = r.text 

    # process the html 
        soup = BeautifulSoup(html, 'html.parser')

        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            # extract the name 
            name = None 
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            # extract the status 
            status = None 
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                status = tag.text

            # extract the shipping cost
            shipping = None
            tags_shipping = tag_item.select('.s-item__shipping, .s-item__freeXDays')
            for tag in tags_shipping:
                shipping = parse_shipping(tag.text)
            
            # extract the price 
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            # extract the free returns 
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns: 
                freereturns = True 

            # extract the number of items sold 
            items_sold = None 
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            item = {
                'name': name,
                'price': price, 
                'shipping': shipping,
                'free_returns': freereturns,
                'items_sold': items_sold,
                'status': status,
            }

            items.append(item)

        print('len(tags_items)=', len(tags_items))
        print('len(items)=', len(items))

    # write the json to a file 
    filename = args.search_term + '.json'
    with open(filename,'w', encoding ='ascii') as f:
        f.write(json.dumps(items))

    # write the csv to a file 
    if args.csv == True:
        n_items = ['name','price','shipping','free_returns','items_sold','status']
        filename = args.search_term + '.csv'
        with open(filename, 'w', encoding = 'utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=n_items)
            writer.writeheader()
            writer.writerows(items)