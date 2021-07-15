from pipeline import pipeline 
from tkinter import filedialog  
import matplotlib.pyplot as plt



def main():
    fileList = []
    fnames = filedialog.askopenfilename()
    fileList.append(fnames)
    while(fnames):
        fnames = filedialog.askopenfilename()
        fileList.append(fnames)
    for f in fileList:
        if(f):
            pipeline(f)
            plt.close('all')
if __name__ == "__main__":
    main()


