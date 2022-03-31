# -*- coding: utf-8 -*-
import numpy as np
import numpy.linalg as LA
import math

def DP(S, ClassNum, SampleNum):
    """
    "Feature extraction for multiclass BCI using canonical variates analysis"
    URL: http://ftp.idiap.ch/pub/reports/2007/galan_2007_wisp.pdf
         http://www.maths.qmul.ac.uk/~bb/CTS_Chapter5_4_Students.pdf
    """
    n = ClassNum*SampleNum
    ChNum = S.shape[0]
    #AVG_mi@k(AVG_mi)とAVG_m@k(AVG_m)を定義
    c = np.size(S, 1)
    AVG_mi = np.zeros([ChNum, ClassNum])
    AVG_m = np.zeros([ChNum, 1])
    #nも求めるため初期化


    cnt = -1
    for i in range(ClassNum):
        for j in range(SampleNum):
            cnt = cnt + 1
            AVG_mi[:, i] = AVG_mi[:, i] + S[:, cnt]
            AVG_m[:, 0] = AVG_m[:, 0] + S[:, cnt]
        AVG_mi[:, i] = AVG_mi[:, i] / SampleNum
    AVG_m[:, 0] = AVG_m[:, 0] / n


    B = np.zeros([ChNum, ChNum])
    W = np.zeros([ChNum, ChNum])

    for i in range(ClassNum):
        B[:, :] = B[:, :] + SampleNum * np.dot((AVG_mi[:, i] - AVG_m), (AVG_mi[:, i] - AVG_m).T)

    cnt = -1
    for i in range(ClassNum):
        for j in range(SampleNum):
            cnt = cnt + 1
            W[:, :] = W[:, :] + np.dot((S[:, cnt] - AVG_mi[:, i]), (S[:, cnt] - AVG_mi[:, i]).T)

    #print(LA.matrix_rank(W))
    #W^(-1)Bを算出
    #invWB = np.dot(LA.pinv(W), B)
    invWB = np.dot(LA.pinv(W), B)

    #w(固有値)とv(固有ベクトル)算出
    w, v = LA.eig(invWB)
    #v = np.abs(v)

    k_1 = ClassNum - 1
    SortIndex = w.argsort()[::-1][0:k_1]

#    A = np.empty([ChNum, k_1])
#    for i in range(k_1):
#        A[:, i] = v[:, SortIndex[i]]
    A = v[:, SortIndex]

    Y = np.dot(S.T, A)
    S = S.T

    T = np.zeros([ChNum, k_1])
    #y = w / np.sum(w)
    y = np.abs(w[SortIndex]) / np.sum(np.abs(w))

    for i in range(ChNum):
        for j in range(k_1):
            cnt = -1
            for k in range(ClassNum):
                bunsi = 0
                bunbo1 = 0
                bunbo2 = 0
                for l in range(SampleNum):
                    cnt = cnt + 1
                    bunsi = bunsi + (S[cnt, i] - np.mean(S[:, i], axis=0)) * (Y[cnt, j] - np.mean(Y[:, j], axis=0))
                    bunbo1 = bunbo1 + np.square((S[cnt, i] - np.mean(S[:, i], axis=0)))
                    bunbo2 = bunbo2 + np.square((Y[cnt, j] - np.mean(Y[:, j], axis=0)))

                T[i, j] = T[i, j] + abs(bunsi / ( np.sqrt(bunbo1) * np.sqrt(bunbo2) ))

    DP = np.zeros([ChNum])

    #print(T)

    bunbo = 0
    for e in range(ChNum):
        for u in range(k_1):
            bunbo = bunbo + y[u] * np.power(T[e, u], 2)


    for u in range(k_1):
        DP[:] = DP[:] + (y[u] * np.power(T[:, u], 2)) / bunbo

    #print(DP)

    return DP
