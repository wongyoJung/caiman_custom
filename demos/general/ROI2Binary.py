from read_roi import read_roi_file
from read_roi import read_roi_zip
import numpy as np
from PIL import Image
import cv2


def ROI2BIN(roifname):
# ex = "D:/twophoton/test/test.roi"
# roifname = "D:/twophoton/CaImAn/demos/general/RoiSet.zip"
    roisarr = read_roi_zip(roifname)
    idx= 0
    img = np.zeros((512, 512),dtype=bool)

    for indx,r in enumerate(roisarr):
        rois = roisarr[r]
        roi_pix = []
        x = rois['x']
        y = rois['y']

        for px in x:
            idx = x.index(px)
            roi_pix.append((px,y[idx]))
                
        for i in range(512):
            for j in range(512):
                cell = (j,i)
                if(cell in roi_pix):
                    img[i][j]=1

    np.save("tmpsave",img)


        # print(test)
    return img
    # im = Image.fromarray(img.reshape((512,512)).astype('uint8')*255)
    # im.show()
def openBIN(BINname):
    test = np.load("tmpsave.npy")
    print(test)



