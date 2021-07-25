
import cv2
import glob
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.sparse
from tkinter import filedialog  


try:
    cv2.setNumThreads(0)
except:
    pass

try:
    if __IPYTHON__:
        # this is used for debugging purposes only. allows to reload classes
        # when changed
        get_ipython().magic('load_ext autoreload')
        get_ipython().magic('autoreload 2')
except NameError:
    pass


import caiman as cm
from caiman.motion_correction import MotionCorrect
from caiman.source_extraction.cnmf import cnmf as cnmf
from caiman.source_extraction.cnmf import params as params
from caiman.utils.utils import download_demo
from caiman.summary_images import local_correlations_movie_offline
from caiman.utils.custom import saveIndividuals
from customUtils import saveCSV 

def main():
    c, dview, n_processes =\
        cm.cluster.setup_cluster(backend='local', n_processes=None,
                                 single_thread=False)
    border_to_0 = 0 if mc.border_nan == 'copy' else mc.border_to_0


    fname_new = "E:/2P_Kim/20210721/G1-8-fasted-Lipid-T1/0721-G1-8-Fasted-Lipid-T1_els__d1_512_d2_512_d3_1_order_F_frames_5000_.mmap"                          
    
    Yr, dims, T = cm.load_memmap(fname_new)
    images = np.reshape(Yr.T, [T] + list(dims), order='C')

    # dataset dependent parameters
    fr = 5            # imaging rate in frames per second
    decay_time = 0.6   # length of a typical transient in seconds
    dxy = (2., 2.)      # spatial resolution in x and y in (um per pixel)
    # note the lower than usual spatial resolution here
    max_shift_um = (12., 12.)       # maximum shift in um
    patch_motion_um = (100., 100.)  # patch size for non-rigid correction in um

    # motion correction parameters
    pw_rigid = True       # flag to select rigid vs pw_rigid motion correction
    # maximum allowed rigid shift in pixels
    max_shifts = [int(a/b) for a, b in zip(max_shift_um, dxy)]
    # start a new patch for pw-rigid motion correction every x pixels
    strides = tuple([int(a/b) for a, b in zip(patch_motion_um, dxy)])
    # overlap between pathes (size of patch in pixels: strides+overlaps)
    overlaps = (24, 24)
    # maximum deviation allowed for patch with respect to rigid shifts
    max_deviation_rigid = 3

    mc_dict = {
        'fnames': fname_new,
        'fr': fr,
        'decay_time': decay_time,
        'dxy': dxy,
        'pw_rigid': pw_rigid,
        'max_shifts': max_shifts,
        'strides': strides,
        'overlaps': overlaps,
        'max_deviation_rigid': max_deviation_rigid,
        'border_nan': 'copy'
    }

    opts = params.CNMFParams(params_dict=mc_dict)
# %%  parameters for source extraction and deconvolution
    p = 1                    # order of the autoregressive system
    gnb = 2                  # number of global background components
    merge_thr = 0.85         # merging threshold, max correlation allowed
    rf = 30
    # half-size of the patches in pixels. e.g., if rf=25, patches are 50x50
    stride_cnmf = 6          # amount of overlap between the patches in pixels
    K = 4                    # number of components per patch
    gSig = [7,7]            # expected half size of neurons in pixels
    # initialization method (if analyzing dendritic data using 'sparse_nmf')
    method_init = 'greedy_roi'
    ssub = 2                     # spatial subsampling during initialization
    tsub = 2                     # temporal subsampling during intialization
    # parameters for component evaluation
    opts_dict = {'fnames': fname_new,
                 'p': p,
                 'fr': fr,
                 'nb': gnb,
                 'rf': rf,
                 'K': K,
                 'gSig': gSig,
                 'stride': stride_cnmf,
                 'method_init': method_init,
                 'rolling_sum': True,
                 'merge_thr': merge_thr,
                 'n_processes': n_processes,
                 'only_init': True,
                 'ssub': ssub,
                 'tsub': tsub}

    opts.change_params(params_dict=opts_dict)
# %% RUN CNMF ON PATCHES
    # First extract spatial and temporal components on patches and combine them
    # for this step deconvolution is turned off (p=0). If you want to have
    # deconvolution within each patch change params.patch['p_patch'] to a
    # nonzero value

    #opts.change_params({'p': 0})
    cnm = cnmf.CNMF(n_processes, params=opts, dview=dview)
    cnm = cnm.fit(images)

    Cns = local_correlations_movie_offline(fname_new,
                                           remove_baseline=True, window=1000, stride=1000,
                                           winSize_baseline=100, quantil_min_baseline=10,
                                           dview=dview)
    Cn = Cns.max(axis=0)
    Cn[np.isnan(Cn)] = 0

    cnm.estimates.Cn = Cn
    # cnm.save(fname_new[:-5]+'_init.hdf5')

# %% RE-RUN seeded CNMF on accepted patches to refine and perform deconvolution
    cnm2 = cnm.refit(images, dview=dview)
    cnm2.estimates.play_movie(images, q_max=99.9, gain_res=2,magnification=2,bpx=border_to_0,include_bck=False)  # background not shown    
        
        # cnm2.estimates.play_movie(images, q_max=99.9, gain_res=2,
        #                           magnification=2,
        #                           bpx=border_to_0,
        #                           include_bck=False)  # background not shown
if __name__ == "__main__":
    main()