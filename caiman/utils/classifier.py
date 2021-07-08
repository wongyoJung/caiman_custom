import math
import numpy as np

def zscore(data,firstlick):
    baseline = data[firstlick*5-2*5*60:firstlick*5]
    mu = np.mean(baseline)
    sig = np.std(baseline)
    zscore = (data-mu)/sig
    response = zscore[firstlick*5:firstlick*5+10*60*5]
    print(np.mean(response))
    if(np.mean(response)>1):
        return 1
    elif(np.mean(response)<-1):
        return -1
    else: 
        return 0
    # print(mu,sig