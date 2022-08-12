#----------------------------------------------------------------------------#
# YGO_deck.py
#
# Code containing Yu-Gi-Oh Card and Deck objects.
#
# Scott Hunter - 31/07/2022
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
"""
File:       YGO_deck.py     
Version:    0.1

#------------------------------Version History-------------------------------#
#----------------------------------------------------------------------------#
#     Version      |      Date       |             Description               #
#----------------------------------------------------------------------------#
#       0.1        |   31/07/2022    |                                       #
#----------------------------------------------------------------------------#
"""
#--------Imports
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
# Homemade
from tools.YGO_Pro_Deck_Scraper import scraper
from tools.config_reader import csv_to_dict

#--------Card Object
class YGO_Card(object):
    """
    Constructs itself from data on the internet (using scraper tool). Takes
    a passcode for a card as an input, as well as an index for the card in
    the Pandas data frame (which holds the data for all cards in the deck).
    """
    
    def __init__(self, passcode, **kw):
        
        # Read in card I.D from arguments dict, also known as passcode
        self.__passcode = passcode
        
        # Selected browser to use
        # default to chrome
        if "browser" not in kw:
            self.__browser = "Chrome"
        else:
            self.__browser = kw["browser"].title()
            
        # webdrivers directory. If not specified, default to a known path
        if "webdriversDir" not in kw:
            self.__webdriversDir = r"tools\webdrivers"
        else:
            self.__webdriversDir = kw["webdriversDir"]
            
        # API url for card info. using f-string
        # default to ygoprodeck api
        if "url" not in kw:
            self.__url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        else:
            self.__url = kw["url"]
        # Add the passcode to the url
        self.__url += f"?id={self.__passcode}"
        
        # Index for pd data frame
        if "n" not in kw:
            self.__n = 0
        else:
            self.__n = kw["n"]
            
        # Request the card data from YGOProdeck website
        self.__data = self.__req_YGOPro()
            
    def __req_YGOPro(self):
        """
        YGO pro website has an API which is avaliable for getting card info.        
        """
        # Data required to find the card. Used as inputs to scraper.
        req_data = {"browser" : self.__browser,
                    "webdriversDir" : self.__webdriversDir,
                    "url" : self.__url
                    }               
        
        # Create the scraper, which loads the html from the api on init
        print("creating scraper")
        s = scraper(**req_data)
        print("Card: " + s.json["data"][0]["name"] + "\n")
        
    # Getter for cardData
    @property
    def data(self):
        return self.__data
 
#--------Deck Object
class YGO_Deck(object):
    """
    Constructs itself from a .ydk deck list which contains a main, extra and
    side decks. The cards in this deck list should be represented by their
    respective passcodes.
    
    The property "deckList" is a dictionary containing three Pandas data
    frames; main, side and extra. Each index in the data frame
    represents the data for a card, and each data point is an attribute of
    it's respective card object.
    """
    
    def __init__(self, deckFilePath):
        
        # Assign file path
        self.__deckFilePath = deckFilePath
        print(f"\nDeck File: {self.__deckFilePath}\n")
        
        # Title deck from file name
        self.__deckTitle = Path(self.__deckFilePath).stem.title()
        self.__deckTitle = self.__deckTitle.replace("_", " ")
        print(f"Deck Title: {self.__deckTitle}")
        
        # Read cards into sub-deck lists
        self.__cardList = self.__read_ydk() 
        
        # Use populate function to populate deck with card list
        self.__deckList = self.__populate()
        
    def __read_ydk(self):
        """
        
        """
        # Initialise card list
        cardList = {"main" : [],
                    "extra" : [],
                    "side" : []
                    }
        
        subDeck = ""
        # Read .ydk file to card list
        with open(self.__deckFilePath, 'r') as ydk:
                for line in ydk:                                       
                    # Define the sub-deck to add to, then skip to next line
                    if "main" in line:
                        subDeck = "main"
                        continue
                    elif "extra" in line:
                        subDeck = "extra"
                        continue
                    elif "side" in line:
                        subDeck = "side"
                        continue          
                    # If line doesn't contain sub-deck, check for empty space
                    else:
                        if line.strip():
                            # If not a blank line, check if comment
                            if "#" in line:
                                continue
                            else:
                                cardList[subDeck].append(line.strip())
                            
                        
        # Convert card list to numpy array
        for key in cardList:
            cardList[key] = np.array(cardList[key])
                        
        return cardList
                
    def __populate(self):
        """
        
        """
        
        # Initialise deck list
        deckList = {"main" : pd.DataFrame(),
                    "extra" : pd.DataFrame(),
                    "side" : pd.DataFrame()
                    }
        
        n = 0 # Index for pandas dataframe
        # Get occurences of each passcode in each sub-deck
        for subDeck in self.__cardList:
            cardCountDict = Counter(self.__cardList[subDeck])
            
            # Convert to deck list
            for passcode in cardCountDict:
                card = YGO_Card(passcode=passcode, n=n)
                count = cardCountDict[passcode]
                
                df = pd.DataFrame(card.data)
                df["count"] = count
                
                deckList[subDeck] = pd.concat([deckList[subDeck], df])
                
                n += 1
                
        return deckList


    # Getter for deck list
    @property
    def deckList(self):
        return self.__deckList
    
    # Getter for deck totals
    @property
    def totals(self):
        totals = []
        for subDeck in self.__cardList:
            totals.append({subDeck : len(self.__cardList[subDeck])})
        return totals
        
d1 = YGO_Deck(r"test_deck.ydk")    