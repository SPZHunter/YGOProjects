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

#--------Card Object
class YGO_Card(object):
    """
    Constructs itself from data on the internet (using scraper tool). Takes
    a passcode for a card as an input, as well as an index for the card in
    the Pandas data frame (which holds the data for all cards in the deck).
    """
    
    def __init__(self, **kw):
        
        # Read in card I.D from arguments dict, also known as passcode
        self.__passcode = kw["passcode"]
        
        # Index for pd data frame
        self.__n = kw["n"]
        
        # Request the card data from YGOProdeck website
        self.__data = self.__req_YGOPro(self.__passcode, self.__n)
            
    def __req_YGOPro(self, passcode, n):
        """
        
        """
        # Pass passcode to requests along with URL
        
    #     # Read in card name
    #     name = #name data
        
    #     # Read in main card type. this will be:
    #     # Monster, Spell, Trap
    #     cardType = {}
    #     cardType["mainType"] = #Main type data
                
    #     # If a monster card
    #     if "Monster" in cardType["mainType"].title():
    #         # Store the attribute/sub-types
    #         attribute = #attribute data e.g Dark
            
    #         cardType["subType1"] = #Sub-type 1 data e.g Machine, Wrym etc.
    #         cardType["subType2"] = #Sub-type 2 data e.g Fusion XYZ etc.
    #         cardType["subType3"] = #Sub-type 3 data e.g Normal, Effect
            
    #         attDef = #Att/def data
    #     # Else if a spell or trap
    #     else:
    #         attribute = #Property data e.g quick-play    
            
    #     # Read in image data
    #     imgData = #image data, maybe an image object/PIL object?
            
        d = {#"imgData" : imgData,
    #         "name" : name,
    #         "cardType" : cardType,
    #         "attribute" : attribute,
    #         "attDef" : attDef,
              "passcode" : passcode
              }
        
        d = pd.DataFrame(data=d, index=[n])
        
        return d
    
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
        
        # Get occurences of each passcode in each sub-deck
        for subDeck in self.__cardList:
            cardCountDict = Counter(self.__cardList[subDeck])
            # Convert to deck list
            n = 0 # Used for pd data frame index, start at 0 and count up
            for passcode in cardCountDict:
                card = YGO_Card(**{"passcode" : passcode, "n" : n})
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