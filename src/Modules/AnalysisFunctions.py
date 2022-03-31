# -*- coding: utf-8 -*-
import numpy as np
import numpy.linalg as LA
import math
from scipy import sparse
from scipy.sparse.linalg import spsolve

#--------------------------------------------------
def zscore(x, axis=None):
    xmean = x.mean(axis=axis, keepdims=True)
    xstd  = np.std(x, axis=axis, keepdims=True)
    zscore = (x-xmean)/xstd
    return zscore
#-----------------------------------------------------
def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result
#---------------------------------------------------
def ftoi(freqnum, maxfreq, freq):
    fi = round(freqnum / maxfreq * freq)
    return fi
#---------------------------------------------------
def ttoi(timenum, maxtime, time):
    ti = round(timenum / maxtime * time)
    return ti
#---------------------------------------------------
def Findvtoi(val, Array):
    if len(Array) == 1:
        return int(0)
    else:
        step = Array[1] - Array[0]
        return int(round((val - Array[0]) / step))
#----------------------------------------------------------
def STFT(data, M = 1024, step = 100):
    myslices = np.zeros([0, M])
    i = 0
    while M+step*i <= data.shape[0]:
        myslices = np.append(myslices, data[0+step*i:M+step*i].reshape(1, -1), axis=0)
        #print(f's: {0+step*i}, e: {M+step*i}')
        i = i + 1;
    #print(f'data shape: {data.shape}, Sliced data shape: {myslices.shape}')

    win = np.hanning(M + 1)[:-1]
    myslices = myslices*win

    myslices = myslices.T
    #print('Shape of `myslice`', myslices.shape)

    spectrum = np.fft.fft(myslices, axis=0)[:M // 2 + 1:-1]
    return spectrum

#---------------------------------------------------------------
def ERSP(spectrum, Time=[], BaseTime=[]):
    S = np.square(np.abs(spectrum))

    #i_start = int(S.shape[1] * BaseTime[0] // Time[1])
    #i_end = int(S.shape[1] * BaseTime[1] // Time[1])

    i_start = Findvtoi(BaseTime[0], Time)
    i_end = Findvtoi(BaseTime[1], Time)
    #print(f'start: {i_start}, end: {i_end}')

    uB = np.zeros([S.shape[0], 1])
    for i in range(i_start, i_end):
        uB = uB + S[:, i].reshape(-1, 1)
    uB = uB / i_end

    S = 10*np.log10(S / uB)
    return S

#------------------------------------------------------------------
def LSM(Datax, Datay, DIM):
    lenx = Datax.shape[0]

    X = np.zeros((DIM+1, lenx))
    for i in range(0, DIM+1):
        for j in range(0, lenx):
            X[i, j] = Datax[j] ** i

    pinv_tXX = np.linalg.pinv(np.dot(X.T, X))
    pinv_tXX_tX = np.dot(pinv_tXX, X.T)
    parameter = np.dot(Datay, pinv_tXX_tX)

    return(parameter)

#--------------------------------------------------------------
def BLC(Datax, Datay, DIM=1, BaseLineIndex='all'):
    #BaseLineIndex = [StartIndex, EndIndex]
    if BaseLineIndex == 'all':
        BaseLineIndex = [0, Datay.shape[0]-1]

    BaseDatay = Datay[BaseLineIndex[0]:BaseLineIndex[1]+1]
    BaseDatax = Datax[BaseLineIndex[0]:BaseLineIndex[1]+1]

    BLp = LSM(BaseDatax, BaseDatay, DIM)
    BLData = np.zeros_like(Datax)

    for i in range(0, BLp.shape[0]):
        BLData = BLData + (Datax ** i) * BLp[i]

    BLCData = Datay - BLData

    return(BLCData)

#----------------------------------------------------
def baseline_als(y, lam, p, niter=10):
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z
#-------------------------------------------------------------------
def AvgComplementNaN(Dict):
    for k in Dict.keys():
        if len(Dict[k].shape) == 3:
            for i0 in range(Dict[k].shape[0]):
                for i2 in range(Dict[k].shape[2]):
                    for i1 in range(Dict[k].shape[1]):
                        if np.isnan(Dict[k][i0, i1, i2]) == True:
                            if i1 == 0:
                                Dict[k][i0, i1, i2] = 0
                                Dict[k][i0, i1, i2] = Dict[k][i0, i1+1, i2]
                                print(f'i1=0:{Dict[k][i0, i1, i2]}')
                            elif i1 == Dict[k].shape[1] - 1:
                                Dict[k][i0, i1, i2] = 0
                                Dict[k][i0, i1, i2] = Dict[k][i0, i1-1, i2]
                                print(f'i1=max:{Dict[k][i0, i1, i2]}')
                            else:
                                Dict[k][i0, i1, i2] = 0
                                Dict[k][i0, i1, i2] = (Dict[k][i0, i1-1, i2] + Dict[k][i0, i1+1, i2]) / 2
                                print(f'i1=?:{Dict[k][i0, i1, i2]}')
        if len(Dict[k].shape) == 4:
            for i0 in range(Dict[k].shape[0]):
                for i1 in range(Dict[k].shape[1]):
                    for i3 in range(Dict[k].shape[3]):
                        for i2 in range(Dict[k].shape[2]):
                            if np.isnan(Dict[k][i0, i1, i2, i3]) == True:
                                if i2 == 0:
                                    Dict[k][i0, i1, i2, i3] = 0
                                    Dict[k][i0, i1, i2, i3] = Dict[k][i0, i1, i2+1, i3]
                                    print(f'i2=0:{Dict[k][i0, i1, i2, i3]}')
                                elif i2 == Dict[k].shape[2] - 1:
                                    Dict[k][i0, i1, i2, i3] = 0
                                    Dict[k][i0, i1, i2] = Dict[k][i0, i1, i2-1, i3]
                                    print(f'i2=max:{Dict[k][i0, i1, i2, i3]}')
                                else:
                                    Dict[k][i0, i1, i2, i3] = 0
                                    Dict[k][i0, i1, i2] = (Dict[k][i0, i1, i2-1, i3] + Dict[k][i0, i1, i2+1, i3]) / 2
                                    print(f'i2=?:{Dict[k][i0, i1, i2, i3]}')
    return Dict

#----------------------------------------------------------
def NaNtoVal(Dict, val=0):
    #data内のNaNを0に置き換える
    for k in Dict.keys():
        Dict[k][np.isnan(Dict[k].astype(np.float64))] = 0
        #print(np.isnan(Dict[k].astype(np.float64)))
    return Dict
