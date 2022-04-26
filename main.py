"""
------------------------------------------------------------------------------
----------------------------------TODO TABLE----------------------------------
Code -->
[ ] Convert Main() to request/response format
[X] Make Clean() use a regular expression NOTE: UNNECESSARY OPTIMIZATION
[ ] Make MatchAho() return an array of JS Object instead of a list of dicts

Cloud -->
[ ] Make sure function works when called in a script

Debugging -->
[*] Test function on more test cases 
[ ] CHECK FOR ERRORS IN EVERY POSSIBLE CREVICE

Documentation -->
[*] Write documentation for code in github repo
[*] Comment code before you lose sanity
------------------------------------------------------------------------------
"""

import ahocorasick
import json

POOLPATH = "./db.csv"
DICTPATH = "./contacts.json"

def Main(request): 
    filePool = open(POOLPATH)
    fileDict = open(DICTPATH)
    
    dict = json.load(fileDict)
    pool = filePool.read()

    print(MatchAho(dict, pool))

    filePool.close()
    fileDict.close()

#Clean phone number data and return it in a format of 10 digits
def Clean(data :str) -> str:
    return data.replace(' ', '').replace('-', '')[-10:]

#Create trie from dict and search in pool, key is used to access phone number in JSON
def MatchAho(dict :list, pool :str, key :str = "number") -> list:
    aho = ahocorasick.Automaton()
    common = [] #List of dicts containing common contacts

    #First loop to insert elements to trie
    insertIndex = 0;
    for obj in dict:
        cleanData = Clean(obj[key])
        aho.add_word(cleanData, (insertIndex, cleanData))
        insertIndex += 1
    
    aho.make_automaton() #Build output and suffix links
    
    #Second loop to search through pool using trie
    for j, (idx, originalValue) in aho.iter(pool):
        i = j - len(originalValue) + 1
        common.append(dict[idx])
        assert pool[i:i + len(originalValue)] == originalValue
    
    return common

#WARN: REMOVE BELOW LINES BEFORE DEPLOYMENT
if __name__ == "__main__":
    Main(None)
