from telnetlib import NOP
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_hastie_10_2
import pickle

mat = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/CLASubjectE1StLRHand.mat') 
with open('CLS_B.pickle', mode='rb') as f:
    data = pickle.load(f)
#all
print(data[1])
print(data[1].shape)

    