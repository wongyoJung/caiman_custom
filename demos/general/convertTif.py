# Necessary library used for this tutorial
import numpy as np

 # For example a particular image in this case would contain (512*512) rows and columns meaning 262,144 pixels
ROWS = 512    
COLS =  512
# Different images have different dimensions. Change it accordingly

# Opening the input image (RAW)
fin = open('E:/2P_Kim/20210714/G1-5/G1-5-DW-30ul_min-wash/Image_001_001.raw')     
print(fin)

# Loading the input image
print("... Load input image")
img = np.fromfile(fin, dtype = np.uint8, count = ROWS * COLS)
print("Dimension of the old image array: ", img.ndim)
print("Size of the old image array: ", img.size)

# Conversion from 1D to 2D array
img.shape = (img.size // COLS, COLS)
print("New dimension of the array:", img.ndim)
print("----------------------------------------------------")
print(" The 2D array of the original image is: \n", img)
print("----------------------------------------------------")
print("The shape of the original image array is: ", img.shape)

# Save the output image
print("... Save the output image")
img.astype('int8').tofile('NewImage.tif')
print("... File successfully saved")
# Closing the file
fin.close()

