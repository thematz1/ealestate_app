import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import abc
import re

import json
import requests
from bs4 import BeautifulSoup
from scraping.geo_to_address import find_address, find_postal

def get_soup_value(value):
    """Returns a sanitized value"""
    sym = r"(,|\$|\+)"

    try:
        string = value.text.strip()
        if string:
            match = re.findall(sym, string)
            if match:
                for m in match:
                    string = string.split(m)
                    string = " ".join(string)
                string = string.split()

    except (TypeError, AttributeError):
        string = None
    try:
        string = int(string)
    except (TypeError, ValueError):
        pass
    try:
        string = int(value)
    except:
        pass

    return string


def check_num(value):
    # Template for bedrooms and bathrooms
    for idx, item in enumerate(value):
        pattern = r'^[a-zA-Z]+'
        check = re.match(pattern, item)
        if check:
            house_num = "".join(value[:idx-1])
            splits = house_num.split()
 
            for s in splits:
                value.strip(s)

            return house_num, value
 
def address_value(value, geo_points):
    """Returns an atomized value"""
    cites = ['Montreal']
    province = ['Quebec']
    # Check for number chunks
    if value:
        regex = r"(?=\B[A-Z])"
        value = re.sub(regex, ", ", value.text)
        
        house_num, address = check_num(value)
        address1 = find_postal(value)
        postal_info = find_address(", ".join(address1), geo_points=geo_points)
        
        print(value)
        print(address1)
        mydict = {
            "house_num": house_num,
            "street": address1[0],
            "city": address1[1],
            "postal_info": postal_info
        }
        
        return mydict


# Work in progress
def locallogic_request(lat, lng):
    """Use locallogic API for location analytics."""
    PARAMS = {
    'lat': lat,
    'lng': lng,
    'headers': {'X-API-KEY': 'API_KEY'}
    }
    data = requests.get('https://api.locallogic.co/v1/scores', params=PARAMS)
    pp(data.json())

class Connector:
    mydict ={
            'list_num': None,
            'address': None,
            'ask_price': None,
            'geo_points': {"lng": None,
                           "lat": None}
        }
        

    def set_header(self, x):
        string = " ".join(x.keys())
        list_num = r"MLNumberVal|ListingDisplayId|listing-location__code"
        address = r"itemprop=\"address\"|class=\"listing-location__address\"|id=\"listingAddress\""
        ask_price = r""
        match = re.search(pattern, string)
        if match:
            mydict['list_num'] = x.pop(list_num.group())
        if match == 'id="listingPrice"':
            print(x['data-value-cad'])
        else:
            print(x[match.group()]) 

    def data(self, mydict):
        head = list(mydict.keys())
        mydict = set_header(mydict)

            
        
        dd.update(dict(map(lambda info: ( info.text.strip(), get_soup_value(info.findNext('div', class_="carac-value")) ), soup.find_all(class_="carac-title"))))

        return dd

    def business_pages(self, html_doc):
        """Scrape the data from business pages."""
        # Parse HTML
        soup = BeautifulSoup(html_doc, 'lxml')
        dataset = self.data(soup)
        # Values for Local Logic and Google Places
        geo_points = dataset['geo_points']

        return dataset
        