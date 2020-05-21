import os
import random
import time
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver import Firefox, DesiredCapabilities, ActionChains
from selenium.webdriver.firefox.options import Options

from scraping.scrapper import Connector

firefox_path = "/Users/mathewzaharopoulos/dev/realestate_api/src/scraping/utilities/geckodriver"

# Launch Browser in private mode. No cookies
o = Options()
o.add_argument('-private')

driver = Firefox(firefox_options=o, executable_path=firefox_path)

driver.install_addon('/Users/mathewzaharopoulos/dev/realestate_api/src/scraping/utilities/canvas_defender-1.1.0-fx.xpi')
driver.install_addon('/Users/mathewzaharopoulos/dev/realestate_api/src/scraping/utilities/disable_webrtc-1.0.23-an+fx.xpi')
driver.install_addon('/Users/mathewzaharopoulos/dev/realestate_api/src/scraping/utilities/random_user_agent-2.2.12-an+fx.xpi')
driver.install_addon('/Users/mathewzaharopoulos/dev/realestate_api/src/scraping/utilities/canvasblocker-1.2-an+fx.xpi')
driver.install_addon('/Users/mathewzaharopoulos/dev/realestate_api/src/scraping/utilities/spoof_timezone-0.2.3-an+fx.xpi')

# Rest for extension settings
driver.get('https://google.ca')
#SETTINGS FOR PRIVATE MODE
time.sleep(40)

driver.get('https://www.centris.ca/en')

#Sleep to select commercial or residential
time.sleep(random.uniform(2,3))
# Close tabs
for handle in driver.window_handles[1:]:
    driver.switch_to.window(handle)
    driver.close()

time.sleep(2)
driver.switch_to.window(driver.window_handles[0])
driver.implicitly_wait(20)
dropdown = driver.find_element_by_css_selector('.fa-search:nth-child(1)')
if not dropdown:
    time.sleep(2)
    driver.implicitly_wait(10)
    dropdown = driver.find_element_by_css_selector('.fa-search:nth-child(1)')

dropdown.click()
driver.implicitly_wait(30)
time.sleep(2)
driver.find_element_by_xpath('//*[@id="dropdownSort"]').click()
driver.implicitly_wait(30)
time.sleep(random.uniform(2.0, 4.0))
driver.find_element_by_xpath("//a[contains(text(),'Most recent')]").click()

c = Connector()
count = 0
page = 0
page_skip = 0

while count < 3000:
    for i in range(page_skip):
        driver.find_element_by_css_selector('.list-order > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4) > a:nth-child(1)').click()
        time.sleep(random.uniform(1, 3))
    page_skip = 0
    if page >= 12:
        driver.find_element_by_css_selector('.list-order > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4) > a:nth-child(1)').click()
        time.sleep(5)
        page = 0
    item = driver.find_elements_by_css_selector('div.description')
    if not item:
        driver.implicitly_wait(20)
        item = driver.find_elements_by_css_selector('div.description')
    driver.implicitly_wait(10)
    item[page].click()
    time.sleep(random.uniform(5.0, 7.0))
    if not driver.page_source:
        time.sleep(random.uniform(4, 7))
        driver.implicitly_wait(20)
    html = driver.page_source
    c.insert_page([html])
    time.sleep(random.uniform(3, 5.0))
    driver.back()
    time.sleep(random.uniform(5.0, 9.0))
    thumbnail = driver.find_elements_by_css_selector('div.description')
    count += 1
    page += 1
    time.sleep(random.uniform(1,3))

print(count)