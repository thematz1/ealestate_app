
Tests included: - business
                - lot
                - condo
                - plex
                - commercial
                - single-home
                - income
"""
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pprint import pprint as pp
import json
from contextlib import contextmanager

from selenium.webdriver import (Firefox, FirefoxOptions,
                                ActionChains, DesiredCapabilities)
from bs4 import BeautifulSoup
import requests

from .utilities import get_soup_value, address_value
from databasing.details import insert_lead


#  create a pool of resources (threads)
# pool = ThreadPool(processes=5)

#  map a function along with the data used by it into the resources pool
# dataset = pool.map(data, soup)     
# 


class FindStructure:

    def __init__(self, soup):
        self.soup = soup
        
    def parse(self, *args, **kwargs):
 
        for key in kwargs.keys():
            for i in kwargs[key]:
                value = eval('self.soup.find(' + key + '="{}")'.format(i))
                if value:
                    return value



class DataParser:
    def __init__(self, soup):
        self.strt = FindStructure(soup)

    def control(self):
        pass

    def unique_id(self):
        id_ = ["ListingDisplayId", "MLNumberVal"]
        class_ = ["listing-location__code"]
        list_num = self.strt.parse(id=id_, class_=class_, key="list_num")
        if list_num:
            return  get_soup_value(list_num)

    def geo_points(self):
        longitude = ["longitude"]
        latitude = ["latitude"]
        realtor = ["listingDirectionsBtn"]
        lng = self.strt.parse(itemprop=longitude)
        lat = self.strt.parse(itemprop=latitude)
        real = self.strt.parse(id=realtor)
        if real:
            regex = r'[^%a-c=\D][^=a-z]\d*'
            real = real['href']
            matches = re.findall(regex, real)
            points = {"lng": float(".".join(matches[-2:])),
                      "lat": float(".".join(matches[-4:-2]))}
            return points

        if lng and lat:
            points = {"lng": float(lng['content']),
                      "lat": float(lat['content'])}
            return points

    def atomic_address(self):
        itemprop = ["address"]
        id_ = ["listingAddress"]
        address = self.strt.parse(itemprop=itemprop, id=id_)
        if address:
            return address

    
    def ask_price(self):
        id_ = ["listingPrice", "BuyPrice"]
        class_ = ["listing-price__amount"]
        # realtor = ["data-value-cad"]
        price = self.strt.parse(id=id_, class_=class_)
        if price: 
            try:
                content = get_soup_value(price['content'])
                return content
            except:
                price = get_soup_value(price)
                if price:
                    r = re.compile(r'\d[0-9]+')
                    return "".join(list(filter(r.match, price)))

                    

    def walkscore(self):
        onclick = ["OpenWalkSocre(this);"]
        walkscore = self.strt.parse(onclick=onclick)    
        if walkscore:
            return get_soup_value(walkscore)
        


class Connector:

    def data_header(self, soup):
        structure = DataParser(soup)
        dd = {
            'list_num': structure.unique_id(),
            'ask_price': structure.ask_price(),
            'walkscore': structure.walkscore(),
            'geo_points': structure.geo_points(),
            'list_address': structure.atomic_address().text,
    
        }
        dd.update(address_value(structure.atomic_address(), geo_points=dd['geo_points']))
        dd.update(dict(map(lambda info: ( info.text.strip(), get_soup_value(info.findNext('div', class_="carac-value")) ), soup.find_all(class_="carac-title"))))

        return dd

    def insert_page(self, html_docs):
        for html_doc in html_docs:
            """Scrape the data from business pages."""
            # Parse HTML
            soup = BeautifulSoup(html_doc, 'lxml')
            dataset = self.data_header(soup)
            print(dataset)
            # Values for Local Logic and Google Places
            geo_points = dataset['geo_points']
            insert_lead(dataset) 

