"""
Initiate functionality test.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_utilities import data_load, load_page
from src.scraping.scrapper import Connector
# from src.databasing.details import insert_home_lead, insert_business_lead, insert_plex_lead


def data_load_test():
    """Test to ensure folder hierachy is corect."""
    command = ['commercial', 'single-home', 'business',
               'lot', 'condo', 'plex', 'income']
    for c in command:
        assert next(data_load(c))


def business_test():
    html = data_load('business')
    for htm in html:
        page = load_page(htm)
        c = Connector()
        c.insert_page(page)


def single_home_test():
    html = data_load('single-home')
    for htm in html:
        page = load_page(htm)
        c = Connector()
        c.insert_page(page)

def plex_test():
    html = data_load('plex')
    for htm in html:
        page = load_page(htm)
        c = Connector()
        c.insert_page(page)

def lot_test():
    html = data_load('lot')
    for htm in html:
        page = load_page(htm)
        c = Connector()
        c.insert_page(page)

def commercial_test():
    html = data_load('commercial')
    for htm in html:
        page = load_page(htm)
        c = Connector()
        c.insert_page(page)


if __name__ == "__main__":
    data_load_test()
    business = business_test()
    home = single_home_test()
    plex = plex_test()
    lot = lot_test()
    commercial = commercial_test()
    