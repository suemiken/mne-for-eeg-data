from telnetlib import NOP
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_hastie_10_2
import pickle

from sympy import HankelTransform

def chenge_format(mat, paradaim):
    if paradaim == 'CLA':
        time_max = 206
        left = np.empty((0, time_max, 22))
        right = np.empty((0, time_max, 22))
        paccive = np.empty((0, time_max, 22))

        marker = np.array(mat['o']['marker'][0][0])
        data = np.array(mat['o']['data'][0][0])

        first = True
        tmp_m = 0
        counter = 0
        for index, m in enumerate(marker[:,0]):
            if m != 99 and m != 0 and m != 92 and m != 91 and first:
                tmp = np.empty((0, 22))
                tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                first = False
                tmp_m = m
            elif m != 99 and m != 0 and m != 92 and m != 91 and not(first):
                tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                
            elif m == 0 and not(first):
                while tmp.shape[0] < time_max:
                    tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                print(tmp.shape)

                if tmp_m == 1:
                    print('left add')
                    left = np.append(left, tmp.reshape(1,-1,22), axis=0)
                    
                elif tmp_m == 2 :
                    print('right add')
                    right = np.append(right, tmp.reshape(1,-1,22), axis=0)
                elif tmp_m == 3:
                    print('paccive add')
                    paccive = np.append(paccive, tmp.reshape(1,-1,22), axis=0)
                print(str(counter)+'回目')
                counter = counter + 1
                first = True
            else:
                NOP
        c_data = {'left_hand':left, 'right_hand':right, 'paccive':paccive}

    elif paradaim == 'HaLT':
        time_max = 206
        left_hand = np.empty((0, time_max, 22))
        right_hand = np.empty((0, time_max, 22))
        paccive = np.empty((0, time_max, 22))
        left_leg = np.empty((0, time_max, 22))
        tongue = np.empty((0, time_max, 22))
        right_leg = np.empty((0, time_max, 22))

        marker = np.array(mat['o']['marker'][0][0])
        data = np.array(mat['o']['data'][0][0])

        first = True
        tmp_m = 0
        counter = 0
        for index, m in enumerate(marker[:,0]):
            if m != 99 and m != 0 and m != 92 and m != 91 and first:
                tmp = np.empty((0, 22))
                tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                first = False
                tmp_m = m
            elif m != 99 and m != 0 and m != 92 and m != 91 and not(first):
                tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                
            elif m == 0 and not(first):
                while tmp.shape[0] < time_max:
                    tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                print(tmp.shape)

                if tmp_m == 1:
                    print('left hand add')
                    left_hand = np.append(left_hand, tmp.reshape(1,-1,22), axis=0)
                    
                elif tmp_m == 2 :
                    print('right hand add')
                    right_hand = np.append(right_hand, tmp.reshape(1,-1,22), axis=0)
                elif tmp_m == 3:
                    print('paccive add')
                    paccive = np.append(paccive, tmp.reshape(1,-1,22), axis=0)
                
                elif tmp_m == 4:
                    print('left leg add')
                    left_leg = np.append(left_leg, tmp.reshape(1,-1,22), axis=0)
                    
                elif tmp_m == 5 :
                    print('tongue add')
                    tongue = np.append(tongue, tmp.reshape(1,-1,22), axis=0)
                elif tmp_m == 6:
                    print('right leg add')
                    right_leg = np.append(right_leg, tmp.reshape(1,-1,22), axis=0)
                print(str(counter)+'回目')
                counter = counter + 1
                first = True
            else:
                NOP
        c_data = {'left_hand':left_hand, 'right_hand':right_hand, 'paccive':paccive, 
        'left_leg':left_leg, 'tongue':tongue, 'right_leg':right_leg}

    elif paradaim == '5F':
        time_max = 265
        
        thumb = np.empty((0, time_max, 22))
        index_finger = np.empty((0, time_max, 22))
        middle_finger = np.empty((0, time_max, 22))
        ring_finger = np.empty((0, time_max, 22))
        pinkie_finger = np.empty((0, time_max, 22))
        
        marker = np.array(mat['o']['marker'][0][0])
        data = np.array(mat['o']['data'][0][0])

        first = True
        tmp_m = 0
        counter = 0

        for index, m in enumerate(marker[:,0]):
            if m != 0 and first:
                tmp = np.empty((0, 22))
                tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                first = False
                tmp_m = m

            elif m != 0 and not(first):
                tmp = np.append(tmp, data[index,:].reshape(1,22), axis=0)
                
            elif m == 0 and not(first):
                while tmp.shape[0] < time_max:
                    tmp = np.append(tmp,  data[index,:].reshape(1,22), axis=0)
                if tmp.shape[0] < time_max + 1:
                    if tmp_m == 1:
                        thumb = np.append(thumb, tmp.reshape(1,-1,22), axis=0)
                        
                    elif tmp_m == 2 :
                        index_finger = np.append(index_finger, tmp.reshape(1,-1,22), axis=0)
                    elif tmp_m == 3:
                        middle_finger = np.append(middle_finger, tmp.reshape(1,-1,22), axis=0)
                    
                    elif tmp_m == 4:
                        ring_finger = np.append(ring_finger, tmp.reshape(1,-1,22), axis=0)
                        
                    elif tmp_m == 5 :
                        pinkie_finger = np.append(pinkie_finger, tmp.reshape(1,-1,22), axis=0)
                counter = counter + 1
                first = True
                print(str(counter)+'回目')
            else:
                NOP
        c_data = {'thumb':thumb, 'index_finger':index_finger, 'middle_finger':middle_finger, 'ring_finger':ring_finger, 'pinkie_finger':pinkie_finger}

    return c_data


mode = '5F'

if mode == 'HaLT':
    save_path = 'datasets/Large_EEG_motor_imagery/pickle_data/HaLT.pickle'
    mat1 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/HaLTSubjectB1602296StLRHandLegTongue.mat') 
    mat2 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/HaLTSubjectB1602186StLRHandLegTongue.mat') 
    mat3 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/HaLTSubjectB1602256StLRHandLegTongue.mat') 
    clsloop = ['left_hand', 'right_hand', 'paccive', 'left_leg', 'tongue', 'right_leg']
elif mode == 'CLA':
    save_path = 'datasets/Large_EEG_motor_imagery/pickle_data/CLA.pickle'
    mat1 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/CLASubjectB1StLRHand.mat') 
    mat2 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/CLASubjectB2StLRHand.mat') 
    mat3 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/CLASubjectB3StLRHand.mat') 

    clsloop = ['left_hand', 'right_hand', 'paccive']
elif mode == '5F':
    save_path = 'datasets/Large_EEG_motor_imagery/pickle_data/5F.pickle'
    mat1 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/5F-SubjectB-151110-5St-SGLHand.mat') 
    mat2 = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/5F-SubjectB-160316-5St-SGLHand.mat') 
    clsloop = ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'pinkie_finger']

data = chenge_format(mat1, mode)
print(data['thumb'].shape)
data2 = chenge_format(mat2, mode)
print(data['thumb'].shape)
if mode == 'HaLT' or mode == 'CLA':
    data3 = chenge_format(mat3, mode)

for i in clsloop:
    data[i] = np.append(data[i], data2[i], axis=0)
    if mode == 'HaLT' or mode == 'CLA':
        data[i] = np.append(data[i], data3[i], axis=0)


# 最も小さいトライアルに合うように削除、X3のチャンネルを削除
sm = [data[i].shape[0] for i in clsloop]
print(sm)
min = np.min(sm)
for i in clsloop:
    while min < data[i].shape[0]:
        data[i] = np.delete(data[i], -1, axis=0)
    data[i] = np.delete(data[i], -1, axis=2)

#３つのファイルのデータを保存
with open(save_path, mode='wb') as f:
    pickle.dump(data, f)

with open(save_path, mode='rb') as f:
    data = pickle.load(f)

# print(data['left_hand'].shape)  
print(data['thumb'].shape)