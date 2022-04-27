"""
------------------------------------------------------------------------------
----------------------------------TODO TABLE----------------------------------
Code -->
[*] Convert Main() to request/response format
[X] Make Clean() use a regular expression NOTE: UNNECESSARY OPTIMIZATION
[ ] Make MatchAho() return an array of JS Object instead of a list of dicts

Cloud -->
[ ] Make sure function works when called in a script

Debugging -->
[*] Test function on more test cases 
[*] CHECK FOR ERRORS IN EVERY POSSIBLE CREVICE
[ ] Print logs every now and then

Documentation -->
[ ] Write documentation for code in github repo
[*] Comment code before you lose sanity
------------------------------------------------------------------------------
"""

import ahocorasick
from google.cloud import storage
import json

def Main(request):
    request_json = request.get_json(silent=True)

    bucketAddr = request.args.bucket if request_json and "bucket" in request_json else "phone-numberdb"
    dbAddr = request.args.db if request_json and "db" in request_json else "db.csv"
    dictAddr = request.args.dict if request_json and "dict" in request_json else "contacts.json"

    #Get data from cloud storage
    client = storage.Client() 
    bucketObj = client.get_bucket(bucketAddr) 
    if not bucketObj:
        return ""

    dbBlob, dictBlob = bucketObj.get_blob(dbAddr), bucketObj.get_blob(dictAddr)
    if not dbBlob or not dictBlob:
        return ""

    dbData, dictData = dbBlob.download_as_string(), dictBlob.download_as_string()
    if not dbData or not dictData:
        return ""
    
    dictDataList = json.loads(dictData)
    matchText =  MatchAho(dictDataList, dbData)
    return str(matchText)

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
        cleanData = Clean(str(obj[key]))
        aho.add_word(cleanData, (insertIndex, cleanData))
        insertIndex += 1
    
    aho.make_automaton() #Build output and suffix links
    
    #Second loop to search through pool using trie
    for j, (idx, originalValue) in aho.iter(str(pool)):
        # i = j - len(originalValue) + 1
        common.append(dict[idx])
    
    return common

#WARN: REMOVE BELOW LINES BEFORE DEPLOYMENT
if __name__ == "__main__":
    Main(None)
