#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for generating the results presented in Figure9-supplement 1
(ROI registration across multiple days)
The script is intended to demonstrate the process that multiday registration
works, rather than performing registration across 3 different days which can
be done at once using the register_multisession function.
@author: epnevmatikakis
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


# %% load spatial components and correlation images for each session

# fnames = download_demo('alignment.pickle')
# with open(fnames, 'rb') as f:
#     A, CI = pickle.load(f)  
# print("####")
# print(A[0])
# # print(type(A[0]))
# print("####")
# print(asdfasdf)

# xxx = np.load("testmulti/xxx.npy", allow_pickle=True)
#xIm = np.array(Image.open('E:/2P_Kim/06012021 fasted SA-SO test/G1-4/G1-4_Fasted-SA-Session-1/STD_G1-4_Fasted_SA-session1.jpg'))

xIm = cv2.imread("E:/2P_Kim/06012021 fasted SA-SO test/G1-4/G1-4_Fasted-SA-Session-1/MAX_G1-4_Fasted_SA-session1.jpg")


print(type(xIm))
print(xIm.shape)


xxx= scipy.sparse.load_npz("G1-4_Fasted_SO_s2.tif.npz")

#yIm = np.array(Image.open('G1-4_Fasted_SO_s2.png').convert('L'))

yyy = scipy.sparse.load_npz("G1-4_Fasted_SA-session1.tif.npz")

CI = [np.zeros((512,512)), np.zeros((512,512))]



print(xxx)
print(scipy.sparse.isspmatrix_csc(xxx))
print(type(xxx))
A=[xxx,yyy]

plt.imshow(xIm)
plt.savefig("testmulti/total.png")

# A is a list where each entry is the matrix of the spatial components for each session
# CI is a list where each entry is the correlation image for each session

# %% normalizing function


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


# %% normalize sum of each component to 1

dims = CI[0].shape
N = 2  # consider only the first three sessions

A = [csc_matrix(A1/A1.sum(0)) for A1 in A[:N]]
masks = [np.reshape(A_.toarray(), dims + (-1,),
         order='F').transpose(2, 0, 1) for A_ in A]



# %% contour plots for the components of each session (Fig. 14a)

print("^^^^^^^^^^^^^^^^^^")
print(A[0])
print("^^^^^^^^^^^^^^^^^^")

lp, hp = np.nanpercentile(CI[0], [5, 98])



# %% register components across multiple days

max_thr = 0.1
A_reg, assign, match = register_multisession(A, dims, CI, max_thr=max_thr)
masks_reg = np.reshape(A_reg, dims + (-1,), order='F').transpose(2, 0, 1)
# %% first compare results from sessions 1 and 2 (Fig. 14b)
# If you just have two sessions you can use the register_ROIs function
print("registerended")
match_1 = extract_active_components(assign, [0], only=False)
match_2 = extract_active_components(assign, [1], only=False)
match_12 = extract_active_components(assign, [0, 1], only=False)

print("match 1   :  ",match_1.shape)
print("match 2   :  ",match_2.shape)

print("match12  :   ",match_12)

print(match)

cl = ['y', 'g', 'r']
labels = ['Both Sessions', 'Session 1 (only)', 'Session 2 (only)']

id=0
for mm in masks[0][match_12]:
    id=id+1
    if(id>0):
        plt.imshow(xIm, vmin=lp, vmax=hp, cmap='gray')
        plt.contour(norm_nrg(mm), levels=[0.95], colors='y', linewidths=1)
        plt.savefig("testmulti/"+str(id)+".png")

