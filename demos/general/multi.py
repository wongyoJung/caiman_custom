from caiman.utils.utils import download_demo
import numpy as np
import matplotlib.pyplot as plt
import caiman as cm
from caiman.base.rois import register_multisession, extract_active_components, register_ROIs
import matplotlib.lines as mlines
from scipy.sparse import csc_matrix
import pickle
import os
import scipy.sparse
from tkinter import filedialog  
from saveasCSV import saveascsv,opencsv

# file_path = download_demo('alignment.pickle')
# infile = open(file_path,'rb')
# A, CI = pickle.load(infile)
# infile.close()


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


print("open sesssion 1 spatio footprint")
ses1_file_path_npz = filedialog.askopenfilename()
print("=================open sesssion 1 calcium traces====================")
ses1_Data = filedialog.askopenfilename()
filename1 = ses1_Data.split("/")[-1]


print("open sesssion 2 spatio footprint")
ses2_file_path_npz = filedialog.askopenfilename()
print("=================open sesssion 2 calcium traces====================")
ses2_Data = filedialog.askopenfilename()
filename2 = ses2_Data.split("/")[-1]

print("open sesssion 3 spatio footprint")
ses3_file_path_npz = filedialog.askopenfilename()
print("=================open sesssion 2 calcium traces====================")
ses3_Data = filedialog.askopenfilename()
filename3 = ses3_Data.split("/")[-1]


f1= scipy.sparse.load_npz(ses1_file_path_npz)
f2 = scipy.sparse.load_npz(ses2_file_path_npz)
f3 = scipy.sparse.load_npz(ses3_file_path_npz)

Data1 = opencsv(ses1_Data)
Data2 = opencsv(ses2_Data)
Data3 = opencsv(ses3_Data)



A=[f1,f2,f3]
CI = [np.zeros((512,512)), np.zeros((512,512)), np.zeros((512,512))]
dims = CI[0].shape

masks = [np.reshape(A_.toarray(), dims + (-1,),
         order='F').transpose(2, 0, 1) for A_ in A]



# %% register components across multiple days

max_thr = 0.1
A_reg, assign, match = register_multisession(A, dims, CI, max_thr=max_thr)
masks_reg = np.reshape(A_reg, dims + (-1,), order='F').transpose(2, 0, 1)
# %% first compare results from sessions 1 and 2 (Fig. 14b)
# If you just have two sessions you can use the register_ROIs function
match_1 = extract_active_components(assign, [0], only=False)
match_2 = extract_active_components(assign, [1], only=False)
match_3 = extract_active_components(assign, [2], only=False)

match_123 = extract_active_components(assign, [0, 1, 2], only=False)

print(match_123)

Data1_active=[]
Data2_active=[]
Data3_active=[]


for c in match_123:
    ses1 = match[0].index(c)
    ses2 = match[1].index(c)
    ses3 = match[2].index(c)

    ses1_active = Data1[ses1]
    ses2_active = Data2[ses2]
    ses3_active = Data3[ses3]

    Data1_active.append(ses1_active)
    Data2_active.append(ses2_active)
    Data3_active.append(ses3_active)

    print("c    ;   ",c)

saveascsv("Active3_"+filename1,Data1_active)
saveascsv("Active3_"+filename2,Data2_active)
saveascsv("Active3_"+filename3,Data3_active)



if not os.path.exists("testmulti/"+filename1+"_triple_multi/"):
    os.makedirs("testmulti/"+filename1+"_triple_multi/")
# if not os.path.exists("testmulti/"+filename2+"/"):
#     os.makedirs("testmulti/"+filename2+"/")
# if not os.path.exists("testmulti/"+filename3+"/"):
#     os.makedirs("testmulti/"+filename3+"/")
idd = 0 
for cell in match_123:
    idd=idd+1
    print(cell)
    index_0 = match[0].index(cell)
    index_1 = match[1].index(cell)
    index_2 = match[2].index(cell)

    mm0 = masks[0][index_0]
    mm1 = masks[1][index_1]
    mm2 = masks[2][index_2]

    plt.contour(norm_nrg(mm0), levels=[0.95], colors='r', linewidths=1)
    plt.contour(norm_nrg(mm1), levels=[0.95], colors='g', linewidths=1)
    plt.contour(norm_nrg(mm2), levels=[0.95], colors='b', linewidths=1)

    plt.savefig("testmulti/"+filename1+"_triple_multi/"+str(idd)+".png")
    plt.clf()

    
