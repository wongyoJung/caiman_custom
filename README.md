CaImAn
======

# CUSTOMIZED algorithm
1. demo_union.py
script for the overall pipeline for motion correction and cnmf for each images
  1) motion correction: used customized parameters 
  - customized parameters
      # WG : we are using 5Hz video 
    fr = 5            
    ## WG : increased the decay time since we used GCaMP6s
    decay_time = 0.6   
    dxy = (2., 2.)      
    max_shift_um = (12., 12.)      
    patch_motion_um = (100., 100.) 
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
    
  2) cnmf
  - customized parameters
      p = 1                    # order of the autoregressive system
      gnb = 2                  # number of global background components
      merge_thr = 0.85         # merging threshold, max correlation allowed
      rf = 30
      # WG : we increased the half-size of patches, since the hypothalamic nuerons are bigger than cortex neurons
      
      # half-size of the patches in pixels. e.g., if rf=25, patches are 50x50
      stride_cnmf = 6          # amount of overlap between the patches in pixels
      K = 4                    # number of components per patch
      gSig = [7,7]            # expected half size of neurons in pixels
      # WG : increased the expected size of neurons

      # initialization method (if analyzing dendritic data using 'sparse_nmf')
      method_init = 'greedy_roi'
      ssub = 2                     # spatial subsampling during initialization
      tsub = 2                     # temporal subsampling during intialization
   3) saveCSV(cnm2.estimates.C,filename) : save the raw calcium trace from CNMF into CSV file
   4)   scipy.sparse.save_npz(filename+'.npz', cnm2.estimates.A) : save the spaiofootprint of each cells into .npz file


2. testmulti.py
compare pair of ROIs from two sessions and take common ROIs and calcium traces from that common ROIs from each sessions
  1) take the common ROIs from given Caiman function
      match_1 = extract_active_components(assign, [0], only=False)
      match_2 = extract_active_components(assign, [1], only=False)
      match_12 = extract_active_components(assign, [0, 1], only=False)

  2) save calcium traces from common ROIs in each session into new csv files
  
    saveascsv("Active_"+filename1,Data1_active)
    saveascsv("Active_"+filename2,Data2_active)

  3) save the common ROIs image into PNG file
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
        



