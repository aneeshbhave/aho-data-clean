# aho-data-clean
Cloud function for stemious to clean up and pattern match data (phone numbers) in a database.

# Data Gen Info
Proprietary code to generate data to test function
## datagen.py
datagen.py is used to generate n lines of n length consisting of random alpha-numeric characters.
Run datagen.py using python 3.x to get usage info.
## numbergen.cs
numbergen.cs is used to generate a CSV files with format of name, phone number with an option for adding errors to phone numbers.
Compile numbergen using a C# compiler and execute without arguements to get usage info, RandomData.txt must be adjacent to compiled exe.

# Purify Data Script
```
import csv

def Main():
    file = open("./db.csv")
    writeTo = open("./dbp.csv", 'w')
    csvRead = csv.reader(file)
    csvWrite = csv.writer(writeTo)

    for row in csvRead:
        row[1] = row[1].replace(" ", "").replace("-", "")[-10:]
        csvWrite.writerow(row)
    


if __name__ == "__main__":
    Main()
```
This small script purifies data from db.csv and writes it to dbp.csv

# What is "pure" data?
Pure data is data that has been converted from various formats into a standardized format.
In this case phone numbers are formated from various formats to be excatly 10 numerical characters long.

# Main python script
This file is the body of the cloud function which operates on files stored on a google cloud bucket.

## Script Tips
Following are some crucial values to change to tweak the cloud function to your desire.

### Change Clean Function
```
def Clean(data :str) -> str:
    return data.replace(' ', '').replace('-', '')[-10:]
```
This function returns a string input formatted to fit the standard 10 digit format for phone numbers.
It does this by removing all spaces, then removing all -'s and getting the last 10 characters of the remainder string.

For Example -
+91 914-619-6969 -> +91914-619-6969 -> +919146196969 -> 9146196969

### Change key for input JSON file
By default the key for accessing an array of objects (list of dicts) passed to the MatchAho() function is "number", call the function
with a key parameter in order to accesss a custom property to match within a JavaScript Object.
```
def MatchAho(dict :list, pool :str, key :str = "number") -> list:
  ...
```
Call function with MatchAho(dict, pool, key) instead of MatchAho(dict, pool)

## Usage
To use this cloud function. Hit it with an HTTP request with the arguements bucket, db, dict
### request.args.bucket
This property is the name of the GCS Bucket from which data will be retrieved from.
### request.args.db
This property is the name of the database file used as the ahocorasick pool (i.e. the database to be searched in)
### request.args.dict
This is the dictionary file for building an Aho-Corasick trie.

# Todo/Plans for the project
See main.py for a ToDo list.
