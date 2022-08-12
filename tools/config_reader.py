#----------------------------------------------------------------------------#
# config_reader.py
#
# Reads config files.
#
# Scott Hunter - 12/08/2022
#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
"""
File:       config_reader.py 
Version:    0.1

#------------------------------Version History-------------------------------#
#----------------------------------------------------------------------------#
#     Version      |      Date       |             Description               #
#----------------------------------------------------------------------------#
#       0.1        |                 |                                       #
#----------------------------------------------------------------------------#
"""
#--------Imports
import csv

#--------csv_to_dict object
class csv_to_dict(object):
    """
    Reads a .csv and maps each row to a dictionary object with keys being
    column headings.
    """
    
    def __init__(self, filePath):
        """
        Takes file path relative to the file creating the object. Include file
        and extension.
        """
        self.__filePath = filePath
        
        self.__outDicts = self.__read()
                
    def __read(self):
        """
        Use csv.reader object to read the config file.
        """
        with open(self.__filePath, newline='', mode='r') as file:
            reader = csv.DictReader(file)
            
            outDicts = [row for row in reader]
            
        return outDicts
    
    # contents property (list of dicts)
    @property
    def contents(self):
        """
        Contents of the csv file in a list of dicts.
        """
        return self.__outDicts