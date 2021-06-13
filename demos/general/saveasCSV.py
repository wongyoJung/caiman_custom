import csv

def saveascsv(filename,activelist):
    with open(filename+".csv", mode='w') as ff:
        writer = csv.writer(ff, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in activelist:
            writer.writerow(row)
        