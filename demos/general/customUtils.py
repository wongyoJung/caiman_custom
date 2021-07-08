import csv
import numpy as np

def saveCSV(data,filename):
    with open(filename+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for d in data:
            writer.writerow(d)
    print("[saved]")


if __name__ == "__main__":
    data =np.random.rand(3,2)
    saveCSV(data,'test2')