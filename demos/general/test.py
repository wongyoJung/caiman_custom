import json
import cv2  # Not actually necessary if you just want to create an image.
import numpy as np
import math
from caiman.utils.classifier import zscore
from PIL import Image
from convertToROI import write_imagej_roi
from pymagej.roi import ROIEncoder, ROIFreehand
import os

directory = 'E:/2P_Kim/06012021 fasted SA-SO test/1-5/G1-5-Fasted-Lick-SA-Session1/AVG_G1-5_Fasted_SA_s1.tif'
im = Image.open(directory)
filename = directory.split("/")[-1]

width = 512
height = 512
imarray = np.array(im)
# gray = cv2.cvtColor(imarray, cv2.COLOR_BGR2GRAY)
imarray = imarray.astype(np.uint8)
# dst = cv2.bitwise_not(imarray)
#cv2.imshow('test',imarray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# Opening JSON file
f = open('G1-5_Fasted_SA_s1.tif.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)

def isNaN(num):
    return num != num
noncell=[1,2,4,5,6,11,14,15,22,33,40,41,42,43,46,47]
# Iterating through the json
id=0
image = np.zeros((height,width,3), np.uint8)
for i, k in enumerate(data.items()):
    # BGimage = np.zeros((height,width,3), np.uint8)
    BGimage=imarray
    cell = k[1]
    cnt = cell['cnt']
    contours=[]
    xs=[]
    ys=[]
    cx=0
    cy=0
    id=id+1
    response = zscore(cell["dF"],303)
    if not(id in noncell):
        if(response==1):
            color=(0,0,255)
        elif(response==-1):
            color=(255,0,0)
        else:
            color=(255,255,255)
        
        for c in cnt:
            if(not isNaN(c[0])):
                x=math.ceil(c[0])
                y=math.ceil(c[1])
                xs.append(x)
                ys.append(y)
                contours.append([math.ceil(c[0]),math.ceil(c[1])])
                # contours.append((math.ceil(c[0]),math.ceil(c[1])))
                # print(x,y)
                cv2.circle(image,(x,y),1,color,-1)
                cv2.circle(BGimage,(x,y),1,color,-1)
                cv2.circle(imarray,(x,y),1,color,-1)

                cx=x
                cy=y
        # ret, thresh = cv2.threshold(image, 127, 255, 0)
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.putText(BGimage, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1,
        #               (255,255,255), 1, cv2.LINE_AA, False) 
        # print(contours)
        # cv2.drawContours(im, [contours], 0, (0,255,0), 3)
        savedir = "result/"+filename+"/"
        fname = savedir+str(id)+".png"
        roiname = savedir+str(id)+".roi"
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        cv2.imwrite(fname,BGimage)
        roi_obj = ROIFreehand(0, 0, 0, 0,xs,ys) # Make ROIRect object specifing top, left, bottom, right
        with ROIEncoder(roiname, roi_obj) as roi:
            roi.write()
            
cv2.imwrite("result/"+filename+"/total.png",image)
cv2.imwrite("result/"+filename+"/overlap.png",imarray)

f.close()

