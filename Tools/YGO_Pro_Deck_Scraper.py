#----------------------------------------------------------------------------#
# YGO_Pro_Deck_Scraper.py
#
# Code to scrape https://ygoprodeck.com/ card database using requests,
# beautiful soup and selenium
#
# Written using Google Chrome vesrion 104, hence using chromium driver.
# Would want to improve for flexibility in future.
#
# Scott Hunter - 11/08/2022
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
"""
File:       YGO_Pro_Deck_Scraper.py  
Version:    0.1

#------------------------------Version History-------------------------------#
#----------------------------------------------------------------------------#
#     Version      |      Date       |             Description               #
#----------------------------------------------------------------------------#
#       0.1        |   11/08/2022    |                                       #
#----------------------------------------------------------------------------#
"""

import requests
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# Assign the web driver using the driver in this project's repository
driver = Chrome(executable_path=r'webdrivers\chromedriver')


