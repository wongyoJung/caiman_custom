#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for multi-registration comparing two session
1) pick raw calcium trace (.csv file), and ROIs(.npz file from demo_union.py) of each sessions
2) take the common ROIs from two session, and save the calcium trace into new csv file
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import caiman as cm
from caiman.base.rois import register_multisession, extract_active_components, register_ROIs
import matplotlib.lines as mlines
import scipy.sparse
from scipy.sparse import csc_matrix
import pickle
import os
from caiman.utils.utils import download_demo
from PIL import Image
import cv2
from saveasCSV import saveascsv,opencsv
import tkinter as tk
from tkinter import filedialog  
import csv
import sys

root = tk.Tk()
root.withdraw()

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)



print("open sesssion 1 spatio footprint")
ses1_file_path_npz = filedialog.askopenfilename()

print("=================open sesssion 1 calcium traces====================")
ses1_Data = filedialog.askopenfilename()
filename1 = ses1_Data.split("/")[-1]

Data1 = opencsv(ses1_Data)


print("open sesssion 2 spatio footprint")
ses2_file_path_npz = filedialog.askopenfilename()

print("=================open sesssion 2 calcium traces====================")
ses2_Data = filedialog.askopenfilename()
filename2 = ses2_Data.split("/")[-1]
Data2 = opencsv(ses2_Data)


CI = [np.zeros((512,512)), np.zeros((512,512))]


def norm_nrg(a_):
    a = a_.copy()
    dims = a.shape
    a = a.reshape(-1, order='F')
    indx = np.argsort(a, axis=None)[::-1]
    cumEn = np.cumsum(a.flatten()[indx]**2)
    cumEn = cumEn/cumEn[-1]
    a = np.zeros(np.prod(dims))
    a[indx] = cumEn
    return a.reshape(dims, order='F')


# normalize sum of each component to 1

dims = CI[0].shape
N = 2  # consider only the first three sessions

A = [csc_matrix(A1/A1.sum(0)) for A1 in A[:N]]
masks = [np.reshape(A_.toarray(), dims + (-1,),
         order='F').transpose(2, 0, 1) for A_ in A]


lp, hp = np.nanpercentile(CI[0], [5, 98])



#  register components across multiple days
max_thr = 0.1
A_reg, assign, match = register_multisession(A, dims, CI, max_thr=max_thr)
masks_reg = np.reshape(A_reg, dims + (-1,), order='F').transpose(2, 0, 1)

match_1 = extract_active_components(assign, [0], only=False)
match_2 = extract_active_components(assign, [1], only=False)
match_12 = extract_active_components(assign, [0, 1], only=False)

Data1_active=[]
Data2_active=[]

for c in match_12:
    ses1 = match[0].index(c)
    ses2 = match[1].index(c)
    ses1_active = Data1[ses1]
    ses2_active = Data2[ses2]
    Data1_active.append(ses1_active)
    Data2_active.append(ses2_active)
    ## WG: take the common ROIs' calcium trace and save into the array (Data1_active and Data2_active)

## WG : save the common ROIs' calcium trace into new csv file
saveascsv("Active_"+filename1,Data1_active)
saveascsv("Active_"+filename2,Data2_active)


if not os.path.exists("testmulti/"+filename1+"/"):
    os.makedirs("testmulti/"+filename1+"/")
if not os.path.exists("testmulti/"+filename2+"/"):
    os.makedirs("testmulti/"+filename2+"/")

## WG : draw the common ROIs into separated folder
id=0
for mm in masks[0][match_12]:
    id=id+1
    if(id>0):
        plt.contour(norm_nrg(mm), levels=[0.95], colors='r', linewidths=1)
        plt.savefig("testmulti/"+filename1+"/"+str(id)+".png")
        plt.clf()
idd=0
for cell in match_12:
    idd=idd+1
    print(cell)
    index = match[1].index(cell)
    mm = masks[1][index]
    plt.contour(norm_nrg(mm), levels=[0.95], colors='g', linewidths=1)
    plt.savefig("testmulti/"+filename2+"/"+str(idd)+".png")
    plt.clf()
    
