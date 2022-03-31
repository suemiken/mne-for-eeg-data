from telnetlib import NOP
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_hastie_10_2
import pickle

mat = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/5F-SubjectB-151110-5St-SGLHand.mat')

# mat = scipy.io.loadmat('./datasets/Large_EEG_motor_imagery/raw_data/CLASubjectF1509163StLRHand.mat')


ch = 21
plt.figure(figsize=(10,8))
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

# 分表記
str_time = 0
sto_time = 35
marker = mat['o']['marker'][0][0][str_time*200*60:sto_time*200*60]#[4 if i == 99 else i for i in np.array(mat['o']['marker'][0][0][str_time*200*60:sto_time*200*60])]
# marker = [5 if i == 91 else i for i in marker]
# marker = [6 if i == 92 else i for i in marker]
ax1.plot(np.arange(str_time,sto_time,1/200/60), np.array(mat['o']['data'][0][0][str_time*200*60:sto_time*200*60, ch]),lw=0.1)
ax2.plot(np.arange(str_time,sto_time,1/200/60), np.array(marker), color='red',lw=0.1)
ax1.set_ylim(-100,100)
# 秒表記
# str_time = 180
# sto_time = 190
# marker = [4 if i == 99 else i for i in np.array(mat['o']['marker'][0][0][str_time*200:sto_time*200])]
# marker = [5 if i == 91 else i for i in marker]
# marker = [6 if i == 92 else i for i in marker]
# ax1.plot(np.arange(str_time,sto_time,1/200), np.array(mat['o']['data'][0][0][str_time*200:sto_time*200, ch]),lw=1
# , label='x3')
# ax2.plot(np.arange(str_time,sto_time,1/200), np.array(marker), color='red',lw=0.1, label='marker')

ax1.set_xlabel("time[m]")
ax1.set_ylabel("X3 chanel signal[uV]")
ax2.set_ylabel("number of marker")
fig.legend()

plt.show()


# マーカー
print(np.array(mat['o']['marker'][0][0])[:,0])

#データ内容
print(np.array(mat['o']['data'][0][0]).shape)
#総サンプル数
print(mat['o']['nS'])
#サンプリング周波数
print(mat['o']['sampFreq'])