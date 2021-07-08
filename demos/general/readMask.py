from scipy import ndimage as ndi
from skimage.morphology import watershed, dilation
from skimage.segmentation import find_boundaries
from skimage.io import imsave, imread
import imageio


import cv2
import glob
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
from glob import glob

def readmask(dir_path):
    expand_method = 'dilation'
    selem = np.ones((3,3))

    # Set the path of the individual masks. Adapt file extension if masks are not saved as .png
    dir_path = 'D:/twophoton/CaImAn/demos/general/rois'
    file_list = glob(dir_path+'/*.png')

    for i in range(len(file_list)):
        # temporarily save the current mask as a boolean array
        temp = np.asarray(imageio.imread(file_list[i]), dtype=bool)
        
        # the csc_matrix has to be initialized before adding the first mask
        if i == 0:
            A = np.zeros((np.prod(temp.shape), len(file_list)), dtype=bool)
            
        # apply dilation or closing to the mask (optional)
        if expand_method == 'dilation':
            temp = dilation(temp, selem=selem)
        elif expand_method == 'closing':
            temp = dilation(temp, selem=selem)
        # print(temp)
        # flatten the mask to a 1D array and add it to the csc_matrix
        A[:, i] = temp.flatten('F')

    print(A)
    return A

if __name__=="__main__":
    readmask('D:/twophoton/CaImAn/demos/general/rois')