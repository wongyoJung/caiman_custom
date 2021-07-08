import csv

def saveascsv(filename,activelist):
    with open(filename+".csv", mode='w',newline="") as ff:
        writer = csv.writer(ff, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in activelist:
            writer.writerow(row)

def opencsv(filename):
    Data1=[]
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        # print(csvreader)
        for row in csvreader:
            r = row[0].split(",")
            intr=[]
            for s in r:
                intr.append(float(s))
            Data1.append(intr)
    return Data1