"""
------------------------------------------------------------------------------
----------------------------------TODO TABLE----------------------------------
Code -->
[*] Convert Main() to request/response format
[X] Make Clean() use a regular expression NOTE: UNNECESSARY OPTIMIZATION
[ ] Make MatchAho() return an array of JS Object instead of a list of dicts
[ ] Make function work for request.args.db being a list of paths instead of a single path

Cloud -->
[ ] Make sure function works when called in a script
[ ] request.args.dict should be a JSON string instead of a path to a file

Debugging -->
[*] Test function on more test cases 
[*] CHECK FOR ERRORS IN EVERY POSSIBLE CREVICE
[ ] Print logs every now and then

Documentation -->
[*] Write documentation for code in github repo
[*] Comment code before you lose sanity
[ ] Add comments for the cloud part of Main()
------------------------------------------------------------------------------
"""

from google.cloud import storage
import ahocorasick
import json


def Main(request):
    requestArgs = request.args
    
    if requestArgs and "bucket" in requestArgs:
        bucketAddr = requestArgs["bucket"]
    else:

        return "bucket arguement not provided"

    if requestArgs and "db" in requestArgs:
        dbAddr = requestArgs["db"]
    else:
        return "db argument not provided"

    if requestArgs and "dict" in requestArgs:
        dict = requestArgs["dict"]
    else:
        return "dict arguement not provided"

    
    #Get data from cloud storage
    client = storage.Client() 
    if not client:
        return "Unable to connect to Bucket"

    bucketObj = client.get_bucket(bucketAddr) 
    if not bucketObj:
        return f"ERROR: {bucketAddr} not found"


    dbBlob = bucketObj.get_blob(dbAddr)
    if not dbBlob:
        return f"ERROR: {dbAddr} not found in {bucketAddr}"

    dbData= dbBlob.download_as_string()
    if not dbData:
        return f"ERROR: {dbAddr} is empty"
    
    #Parse dict (JSON Data) and match
    dictData = json.loads(str(dict))

    matchText =  MatchAho(dictData, dbData)
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
        cleanData = Clean(str(obj[key])) #Type-casting in case input data is an int
        aho.add_word(cleanData, (insertIndex, cleanData))
        insertIndex += 1
    
    aho.make_automaton()
    
    #Second loop to search through pool using trie
    for j, (idx, originalValue) in aho.iter(str(pool)):
        # i = j - len(originalValue) + 1
        common.append(dict[idx])
    
    return common

#WARN: REMOVE BELOW LINES BEFORE DEPLOYMENT
if __name__ == "__main__":
    Main(None)
