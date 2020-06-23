'''
                              6-Letter Pypher 1.0                               
                    Copyright (c) 2015 Ben Goldsworthy (rumps)                   
                                                                               
   A program to encode and decode text using a 6-letter cipher and given
   keyword.                                                    
                                                                               
   6-Letter Pypher is free software: you can redistribute it and/or modify        
   it under the terms of the GNU General Public License as published by        
   the Free Software Foundation, either version 3 of the License, or           
   (at your option) any later version.                                         
                                                                               
   6-Letter Pypher is distributed in the hope that it will be useful,            
   but WITHOUT ANY WARRANTY; without even the implied warranty of              
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               
   GNU General Public License for more details.                                
                                                                               
   You should have received a copy of the GNU General Public License           
   along with 6-Letter Pypher.  If not, see <http://www.gnu.org/licenses/>.      
'''

import numpy as np
import string
import random
import re
import pickle
import operator

# A dictionary used for indexing characters in the initial alphanumeric grid
alphaNumCoords = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}

def encodePlaintext():
   """Coordinates the steps involved in encoding plaintext and prints results."""
   fileName = genFileName(4)
   alphaNumGrid = makeAlphaNumGrid(fileName)

   plaintext = enterPlaintext()
   keyword = sorted(enterKeyword(len(plaintext)))
   print "\nEncoding", plaintext, "with keyword", getKeywordString(keyword), "...\n"
   print "--Alphanumeric grid--\n", alphaNumGrid

   ciphertext = getTransitionalCiphertext(plaintext, alphaNumGrid)
   print "Transitional ciphertext:", ciphertext, "\n"

   keywordGrid = getKeywordGrid(ciphertext, keyword, 'encode')
   print "--Keyword grid--\n", keywordGrid
   ciphertext = getCiphertext(keywordGrid)
   print "Final ciphertext:", ciphertext, "\nEncoded using grid", fileName
def decodeCiphertext():
   """Coordinates the steps involved in decoding ciphertext and prints results."""
   filename = raw_input("Enter grid code: ")
   alphaNumGrid = pickle.load(open("Ciphers/"+filename+".p", "rb" ))
   
   ciphertext = enterCiphertext()
   keyword = enterKeyword(len(ciphertext)/2)
   keywordGrid = getKeywordGrid(ciphertext, keyword, 'decode')
   print "\nDecoding", ciphertext, "with keyword", getKeywordString(keyword), "using grid", filename, "...\n"
   print "--Keyword grid--\n", keywordGrid
   
   plaintext = getTransitionalPlaintext(keywordGrid)
   print "Transitional plaintext:", plaintext, "\n"
   
   print "--Alphanumeric grid--\n", alphaNumGrid
   plaintext = getPlaintext(plaintext, alphaNumGrid)
   print "Final plaintext:", plaintext
def showCredits():
   """Prints the credits and copyright information."""
   print "*" * 80
   print "\t\t\t6-Letter Pypher 1.0"
   print "\t\tCopyright (c) 2015 Ben Goldsworthy (rumps)\n"
   print " A program to encode and decode text using a 6-letter cipher and given\n keyword.\n "
   print " 6-Letter Pypher is free software: you can redistribute it and/or modify\n it under the terms of the GNU General Public License as published by\n the Free Software Foundation, either version 3 of the License, or\n (at your option) any later version.\n "
   print " 6-Letter Pypher is distributed in the hope that it will be useful,\n but WITHOUT ANY WARRANTY; without even the implied warranty of\n MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n GNU General Public License for more details.\n "
   print " You should have received a copy of the GNU General Public License\n along with 6-Letter Pypher.  If not, see <http://www.gnu.org/licenses/>."
   print "*" * 80
   
def makeAlphaNumGrid(fileName):
   """Generates an alphanumeric grid and pickles it for later consumption."""
   vals = list(string.ascii_uppercase + string.digits)
   random.shuffle(vals)
   grid = np.array(vals).reshape(6,6)
   pickle.dump(grid, open("Ciphers/"+fileName+".p", "wb"))
   return grid
def genFileName(n):
   """Generates a randomised filename for the pickle."""
   name = ""
   for x in range(n): name += random.choice(string.letters + string.digits)
   return name
def findLetter(letter, x):
   """Finds a letter in the alphanumeric grid and returns its coordinates."""
   for i in range(6):
      for j in range(6):
         if x[i][j] == letter:
            return alphaNumCoords[j] + alphaNumCoords[i]
   return ''
   
def enterPlaintext():
   """Takes and validates plaintext entry from the user. Returns valid entry
   stripped of whitespace.
   """
   plaintext = ""
   # RegEx for non-alphanumeric characters
   alphaNum = re.compile(r'[^a-zA-Z0-9 ]')
   
   while plaintext == "":
      err = False
      plaintext = raw_input("What is your plaintext? ").upper()
      if alphaNum.search(plaintext) != None:
         print "ERR: Plaintext must contain characters A-Z or 0-9"
         err = True
      if err == True: plaintext = ""
   # Includes RegEx to strip whitespace
   return re.sub(r'\W+', '', plaintext)
def enterKeyword(plaintextLen):
   """Takes and validates keyword entry from the user. Returns an list of 
   indexed tuples representing the keyword string.
   """
   keyword = ""
   # RegEx for detecting repeated or invalid characters
   rpt = re.compile(r'.*(.).*\1.*')
   alpha = re.compile(r'[^a-zA-Z]')
   
   while keyword == "":
      err = False
      keyword = raw_input("What is the keyword? ").upper()
      if alpha.search(keyword) != None:
         print "ERR: Keyword must contain characters A-Z"
         err = True
      if rpt.match(keyword):
         print "ERR: Keyword must contain no repeating characters"
         err = True
      if plaintextLen % len(keyword) != 0:
         print "ERR: Length of plaintext (", plaintextLen, \
         ") must be divisible by length of keyword (", len(keyword), ")"
         err = True
      if err == True: keyword = ""
   return getKeyword(keyword)
def enterCiphertext():
   """Takes and validates ciphertext entry from the user."""
   ciphertext = ""
   # RegEx to detect invalid characters
   alphaNum = re.compile(r'[^A-F]')
   
   while ciphertext == "":
      err = False
      ciphertext = raw_input("Enter ciphertext: ").upper()
      if alphaNum.search(ciphertext) != None:
         print "ERR: Ciphertext must contain characters A-F"
         err = True
      if err == True: ciphertext = ""
   return ciphertext
  
def getKeyword(keyword):
   """Returns a sorted list of tuples representing the keyword string."""
   return sorted(enumerate(keyword), key=operator.itemgetter(1))
def getKeywordGrid(ciphertext, keyword, mode):
   """Generates the keyword grid from the entered keyword, then returns it
   sorted appropriately (either alphabetically for encoding or back to keywordly
   for decoding).
   """
   keywordCipher = [x[1] for x in keyword]
   keywordLength = len(keywordCipher)
   for letter in ciphertext:
      keywordCipher.append(letter)
   
   yLength = len(ciphertext)/keywordLength + 1
   keywordGrid = np.array(keywordCipher).reshape(yLength, keywordLength)
   
   if mode == 'encode':
      return keywordGrid[:, np.array(orderKeyword([x[1] for x in keyword]))]
   elif mode == 'decode':
      return keywordGrid[:, np.array([x[1] for x in getUnorderedKeyword(keyword)])]
def orderKeyword(keyword):
   """Orders the keyword characters alphabetically and returns the new 
   indicies.
   """
   orderedKeyword = sorted(enumerate(keyword), key=operator.itemgetter(1))
   return [x[0] for x in orderedKeyword]
def getUnorderedKeyword(keyword):
   originalKeyword = sorted(keyword)
   currIndex = 0
   mylist = []
   for i in range(len(getKeywordString(keyword))):
      mylist.append((keyword[i][0], originalKeyword[i][0]))
   return sorted(mylist)
      
def getKeywordString(keyword):
   """Extracts the keyword string from the list of tuples representing it."""
   keywordString = ""
   for x in sorted(keyword): keywordString += x[1]
   return keywordString 
def getTransitionalCiphertext(plaintext, alphaNumGrid):
   """Gets the ciphertext created by applying the alphanumeric grid to the
   entered plaintext.
   """
   ciphertext = ""
   for letter in plaintext:
      ciphertext += findLetter(letter, alphaNumGrid)
   return ciphertext
def getCiphertext(keywordGrid):
   """Gets the final ciphertext created by applying the keyword grid to the
   transitional ciphertext.
   """
   ciphertext = ""
   for row in keywordGrid[1:].tolist():
      for letter in row:
         ciphertext += letter
   return ciphertext
def getTransitionalPlaintext(keywordGrid):
   """Splits the transitional plaintext into 2-character chunks."""
   tpt = ""
   double = 0
   for x in keywordGrid[1:]:
      for x in x:
         if double == 2:
            double = 0
            tpt += " "
         tpt += x
         double += 1
   return tpt
def getPlaintext(plaintext, alphaNumGrid):
   """Gets the final plaintext created by reversing the application of the
   alphanumeric grid to the original plaintext.
   """
   finalPlaintext = ""
   for x in plaintext.split():
      for k,v in alphaNumCoords.iteritems():
         if v == x[1]: xcoord = k
         if v == x[0]: ycoord = k
      finalPlaintext += alphaNumGrid[xcoord][ycoord]
   return finalPlaintext

def menu():
   """Displays the option menu for the user and takes input."""
   option = ''
   while option != 4:
      print "\nSelect action:"
      print "\t1. Encode plaintext"
      print "\t2. Decode plaintext"
      print "\t3. License & Credits"
      print "\t4. Exit\n"
      option = raw_input("Choice: ")
      if option == '1':
         encodePlaintext()
      elif option == '2':
         decodeCiphertext()
      elif option == '3':
         showCredits()

# Calls the menu on program start
menu()
