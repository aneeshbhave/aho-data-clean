import sys, os, random

def PrintUsage():
    print("Usage: python datagen <file-name>")
    exit(-1)

def PrintErr(message):
    print("[ERROR]: " + message)
    exit(-1)

argc = len(sys.argv)

if argc != 2:
    PrintUsage()

lines = int(input("Enter number of lines: "))
lenline = int(input("Enter length of each line: "))

filePath = sys.argv[1]

alpha = "abcdefghijklmnopqrstuvwxyz" 
chars = alpha + alpha.upper() + "0123456789"
totalChars = len(chars)

if os.path.exists(filePath):
    PrintErr("File already exists.")
else:
    f = open(filePath, "w")

for i in range(lines):
    line = ""
    for j in range(lenline):
        line += chars[random.randint(0, totalChars - 1)]
    line += '\n'
    f.write(line)

