"""
------------------------------------------------------------------------------
----------------------------------TODO TABLE----------------------------------

Cloud -->
[ ] Convert Main() to request/response format
[ ] Make sure function works when called in a script

Debugging -->
[ ] Test function on more test cases 
[ ] CHECK FOR ERRORS IN EVERY POSSIBLE CREVICE

Documentation -->
[ ] Write documentation for code in github repo
[ ] Comment code before you lose sanity
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

def Clean(data :str) -> str:
    return data.replace(' ', '').replace('-', '')[-10:]

def MatchAho(dict :list, pool :str, key :str = "number") -> list:
    aho = ahocorasick.Automaton()
    common = []

    insertIndex = 0;
    for obj in dict:
        cleanData = Clean(obj[key])
        aho.add_word(cleanData, (insertIndex, cleanData))
        insertIndex += 1
    
    aho.make_automaton()

    for j, (idx, originalValue) in aho.iter(pool):
        i = j - len(originalValue) + 1
        common.append(dict[idx])
        assert pool[i:i + len(originalValue)] == originalValue
    
    return common

#!REMOVE BELOW LINES BEFORE DEPLOYMENT
if __name__ == "__main__":
    Main(None)
