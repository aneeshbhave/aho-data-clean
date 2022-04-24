import csv

def Main():
    file = open("./dbimpure.csv")
    writeTo = open("./db.csv", 'w')
    csvRead = csv.reader(file)
    csvWrite = csv.writer(writeTo)

    for row in csvRead:
        row[1] = row[1].replace(" ", "").replace("-", "")[-10:]
        csvWrite.writerow(row)
    


if __name__ == "__main__":
    Main()
