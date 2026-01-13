#!/usr/bin/env python3

def optimalSplit(word):
  #creating 2d array based on string length
  global subStrings
  global posSolutions
  global ignoreThese 
  ignoreThese = []
  wordCount = 0
  c = [[]]
  n = len(word)
  for i in range (n - 1):
    c.append([])

  for i in range (n):
    for j in range (n):
      c[i].append([])

  #populating table from "bottom-right"
  for i in range(n-1, -1, -1):
    for j in range (n-1, i-1, -1):
      subString = word[i: j+1]
      #print(subString + " ")
      if subString in wordDict:
        
        c[i][j] = 1
        continue
        
  wordCount = 9999
  prev = []

  """#printing table for testing 
  for i in range(n):
    for j in range(n):
      print(c[i][j], end = " ")
    print()
  print()"""
  
  #populating list of possible solutions 
  while wordCount > 0:
    wordCount = wordSearch(c, 0, n-1, prev)
    if wordCount > 0:
      list = [wordCount, subStrings]
      posSolutions.append(list)
      subStrings = []
      prev = []
      
  """#printing for troubleshooting, remove when done
  for x,y in posSolutions:
    print("Possible solution: " + str(x))
    for p,q in y:
      print(word[p:q+1], end = " ")
    print()
  print("ignoreThese: " + str(ignoreThese))"""
  
  
  
  return wordCount

#This function takes 3 parameters, a 2d table, index i and index j. It will travers the row (i) from right to left, looking for the first "1". This one will indicate the word in the table from i to j. I will recursively call itself with a new row (i) to continue looking for the next largest word in that substring. 
#This function will return the i and j where c[i:j] should splice the string into a substring that is in the dictionary
#may need a more appropriate name
def wordSearch (c, i, j, prev):
  #print("i: %d\tj: %d\tprev: " % (i, j) + str(prev) )
  x = j
  prev.append(i)
  if (i == 0 and j == 0):
    return 0
  elif (i >= j):
    return 0
  for x in range(j, i-1, -1):
    #"If in first row and this '1' has already been traversed, skip this '1'"
    if i == 0 and x in ignoreThese: 
      continue
    if c[i][x] == 1:
      #"If we got here, this '1' has't been traversed"
      #"If we are still on first row, add this one to the list of '1's already traversed"
      if i == 0:
        ignoreThese.append(x)
      subStrings.append([i,x])
      return 1 + wordSearch(c, x + 1, len(c[0])-1, prev)
  #Going back to previous row if no ones are found
  if len(subStrings) > 0:
    del subStrings[-1]
    del prev[-1]
    return -1 + wordSearch(c, prev[-1], x-2, prev)
  return 0
  

def pickOptimalSol(posSolutions, word):
  numSol = len(posSolutions)
  if numSol > 0:
    minWord = posSolutions[0][0]
    minIndex = 0
  
    for i in range(numSol):
      if posSolutions[i][0] < minWord:
        #print(posSolutions[i][1][len(posSolutions[i][1])-1])
        if posSolutions[i][1][len(posSolutions[i][1])-1][1] == len(word) - 1:
          minIndex = i
  
    global wordCount
    wordCount = posSolutions[minIndex][0]
    global subStrings
    subStrings = posSolutions[minIndex][1]
    
  else:
    wordCount = 0
    subStrings= []
"""
BEGINING OF MAIN FUNCTION
"""
#var declarations
wordList = []
wordDict = {}

#creating a list of words from dictionary file
with open ("aliceInWonderlandDictionary.txt") as f:
  content = f.read()
  wordList = content.split()


#creating a dictionary with empty key value
wordDict = dict.fromkeys(wordList)

#creating a list of words from intput file
with open("input.txt") as f:
  content = f.read()
  wordList = content.split()


#finding optinal solution
for word in wordList:
  posSolutions = []
  print("Word: %s" %(word))
  subStrings = []
  wordCount = optimalSplit(word)
  pickOptimalSol(posSolutions, word)

  ###################
  #printing solution#
  ###################
  
  #if word cannot be split
  if (wordCount == 0):
    print("Cannot be split")
    print()
  #if word splits in 2 but one of them is invalid 
  elif (subStrings[len(subStrings) - 1][1] != len(word) - 1) :
    print("Cannot be split")
    print()
  #else is a valid word
  else:
    print("Optimal words: %d" % (wordCount))
    for x,y in subStrings:
      print(word[x:y+1], end = " ")
    print()
    print()
