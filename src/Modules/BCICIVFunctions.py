# -*- coding: utf-8 -*- 
import numpy as np
from scipy import io

def ImportData(filename):
    #######################
    c1 = 'class1'
    c2 = 'class2'
    c3 = 'class3'
    c4 = 'class4'
    eo = 'eye_open'
    ec = 'eye_close'
    em = 'eye_move'
    key = (c1, c2, c3, c4, eo, ec, em)
    #######################
    matdata = io.loadmat(filename, squeeze_me=True)
    DataBCI = {'class1' : np.array(matdata["class1"]),
            'class2' : np.array(matdata["class2"]),
            'class3' : np.array(matdata["class3"]),
            'class4' : np.array(matdata["class4"]),
            'eye_open' : np.array(matdata["eye_open"]),
            'eye_close' : np.array(matdata["eye_close"]),
            'eye_move' : np.array(matdata["eye_move"])}

    return DataBCI, key
