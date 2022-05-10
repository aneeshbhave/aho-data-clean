"""
----------------------------------TODO TABLE----------------------------------
Code -->
[*] Convert Main() to request/response format
[X] Make Clean() use a regular expression NOTE: UNNECESSARY OPTIMIZATION
[X] Make MatchAho() return an array of JS Object instead of a list of dicts NOTE: Use JSON.Parse() when called
<<<<<<< HEAD
[*] Make function work for request.args.db being a list of paths instead of a single path
=======
[ ] Make function work for request.args.db being a list of paths instead of a single path
>>>>>>> 0f631f1187a28927cab3d5f97b240062d1ce8965

Cloud -->
[*] Make sure function works when called in a script
[*] request.args.dict should be a JSON string instead of a path to a file
[*] Make function use POST request

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
import ahocorasick, phonenumbers, json

def Main(request):
    if request.method != "POST":
        return "ERR: Request type is not POST"

    contentType = request.headers["content-type"]
    if contentType != "application/json":
        return "ERR: Request body must be JSON"

    requestJSON = request.get_json(silent=True)
    if not requestJSON:
        return "ERR: Request body must not be empty"

    if "bucket" in requestJSON:
        bucketAddr = requestJSON["bucket"]
    else:
        return "ERR: bucket arguement not provided"
    if "db" in requestJSON:
        dbAddr = requestJSON["db"]
    else:
        return "ERR: db arguement not provided"
    if "dict" in requestJSON:
        dict = requestJSON["dict"]
    else:
        return "ERR: dict arguement not provided"
    
    #Get data from cloud storage
    client = storage.Client() 
    if not client:
        return "ERR: Unable to connect to Bucket"

    bucketObj = client.get_bucket(bucketAddr) 
    if not bucketObj:
<<<<<<< HEAD
        return f"ERR: {bucketAddr} not found"
    
    if not dbAddr:
        return f"ERR: {dbAddr} is empty"
    dbAddrList = dbAddr
=======
        return f"ERROR: {bucketAddr} not found"
    
    if not dbAddr:
        return f"ERROR {dbAddr} is empty"
    dbAddrList = json.loads(dbAddr)
>>>>>>> 0f631f1187a28927cab3d5f97b240062d1ce8965
    
    dbList = []
    for addr in dbAddrList:
        dbBlob = bucketObj.get_blob(addr)
        if not dbBlob:
<<<<<<< HEAD
            return f"ERR: {dbAddr} not found in {bucketAddr}"
        dbData = dbBlob.download_as_string()
        if not dbData:
            return f"ERR: {addr} is empty"
        dbList.append(str(dbData))

    #Parse dict (JSON Data) and matchText
    dictData = dict
=======
            return f"ERROR: {dbAddr} not found in {bucketAddr}"
        dbData = dbBlob.download_as_string()
        if not dbData:
            return f"ERROR: {addr} is empty"
        dbList.append(str(dbData))

    #Parse dict (JSON Data) and matchText
    dictData = json.loads(str(dict))
>>>>>>> 0f631f1187a28927cab3d5f97b240062d1ce8965
    
    matchText =  MatchAho(dictData, dbList)
    return str(matchText)

#Clean phone number data and return it in a format of 10 digits
def Clean(data :str) -> str:
    if data[0] != '+' and len(data) != 10:
        data = '+' + data
    try:
        ret = str(phonenumbers.parse(data, None).national_number)
    except:
<<<<<<< HEAD
        try:
            translateDict = {
                    '-': '',
                    ' ': '',
                    '(': '',
                    ')': '',
                    }
            translated = data.translate(translateDict)
            return translated[-10:]
        except:
            return ""
=======
        translateDict = {
                '-': '',
                ' ': '',
                '(': '',
                ')': '',
                }
        translated = data.translate(translateDict)
        return translated
>>>>>>> 0f631f1187a28927cab3d5f97b240062d1ce8965
    return ret

#Create trie from dict and search in pool, key is used to access phone number in JSON
def MatchAho(dict :list, poolList :list, key :str = "number") -> list:
    aho = ahocorasick.Automaton()
    common = [] #List of dicts containing common contacts

    #First loop to insert elements to trie
    insertIndex = 0;
    for obj in dict:
        cleanData = Clean(str(obj[key])) #Type-casting in case input data is an int
        aho.add_word(cleanData, (insertIndex, cleanData))
        insertIndex += 1
    
    aho.make_automaton()
    
    for pool in poolList:
        #Second loop to search through pool using trie
        for j, (idx, val) in aho.iter(str(pool)):
            # i = j - len(originalValue) + 1
            common.append(dict[idx])
    
    return common

#WARN: REMOVE BELOW LINES BEFORE DEPLOYMENT
# if __name__ == "__main__":
    # Main(None)
