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
#--------Imports
import json
from pathlib import Path
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
# Homemade
from tools.config_reader import csv_to_dict

#--------Scraper object
class scraper(object):
    """
    """
    
    def __init__(self, **kw):
        
        # webdriver path passed in
        webdriversDir = kw["webdriversDir"]
        
        # Set up the driver
        # if selected browser is chrome
        if kw["browser"].title() == "Chrome": 
            options = ChromeOptions()
            options.headless = True
            self.__driver = Chrome(executable_path=webdriversDir + '\chromedriver', 
                        options=options)
        # Default to using chrome
        else:
            options = ChromeOptions()
            options.headless = True
            self.__driver = Chrome(executable_path=webdriversDir + '\chromedriver', 
                        options=options)
        
       
        # Assign the URL
        self.__url = kw["url"]
        
        # Get the web page
        print(f"requesting from: {self.__url}")
        self.__driver.get(self.__url)
        
        # Create beautiful soup object
        print("parsing to beautiful soup 4")
        soup = bs(self.__driver.page_source, 'lxml')
        
        # Parse soup to JSON
        print("parsing to json")
        self.__json = json.loads(soup.get_text())
        
        
    @property
    def json(self):
        return self.__json
        





























