# -*- coding: utf-8 -*-
import numpy as np

#-------------------------------------------------------
def ShuffleDataSet(Data, Label, *, seed=0):
    #トライアルデータをランダムにシャッフル
    np.random.seed(seed) # 乱数のシード設定
    indices = np.random.permutation(len(Data))
    Data_s = Data[indices] # データの順序をランダムに並び替え
    Label_s = Label[indices]
    return Data_s, Label_s
#-----------------------------------------------------------------------
def ShapeDataForMachineLearn(OriginData, *, LabelDict, ChNum, TrialNum,
                        TimeSampleNum, FrqSampleNum=None, MODE='TIME_CH'):
# OrginData > {'クラス' : np.array[チャネル, 時系列, トライアル], ...}
#           or {'クラス' : np.array[チャネル, 周波数列, 時系列, トライアル], ...}
# LabelDict > 辞書型{'クラス名' : int(ラベル番号), ...}
# ChNum > int(チャネル数)
# TrialNum > int(トライアル数)
# TimeSampleNum > int(時系列データのサンプル数)
# FrqSampleNum > int(時間周波数データのサンプル数)
    #クラス数を確認
    ClassNum = len(OriginData)
    #ラベル配列「LabelArray」に「data1」に対応したラベルを付与
    Label = np.zeros([TrialNum*ClassNum])

    #時間サンプルとチャネルの次元をまとめて1次元にするなら > 「MODE」='TIME_CH' or'TIME_CH2'
    #時間サンプルと周波数サンプルとチャネルの次元をまとめて1次元にするなら > 「MODE」='TIME_FRQ_CH'
    if MODE == 'TIME_CH2':
        #2次元データ配列作成
        Data = np.zeros([TrialNum*ClassNum, ChNum*TimeSampleNum])

        tc_cnt = -1
        for k, l in LabelDict.items():
            for tryi in range(0, TrialNum):
                tc_cnt = tc_cnt + 1
                Data[tc_cnt, :] = OriginData[k].reshape(-1, TrialNum)[:, tryi]
                Label[tc_cnt] = l
        return Data, Label

    elif MODE == 'TIME_CH':
        #2次元データ配列作成
        Data = np.zeros([TrialNum*ClassNum, ChNum*TimeSampleNum])

        tc_cnt = -1
        for k, l in LabelDict.items():
            for tryi in range(0, TrialNum):
                tc_cnt = tc_cnt + 1
                s_cnt  = -1
                for ci in range(0, ChNum):
                    for ti in range(0, TimeSampleNum):
                        s_cnt = s_cnt + 1
                        Data[tc_cnt, s_cnt] = OriginData[k][ci, ti, tryi]
                        Label[tc_cnt] = l
        return Data, Label

    elif MODE == 'TIME_FRQ_CH':
        #2次元データ配列作成
        Data = np.zeros([TrialNum*ClassNum, ChNum*FrqSampleNum*TimeSampleNum])

        tc_cnt = -1
        for k, l in LabelDict.items():
            for tryi in range(0, TrialNum):
                tc_cnt = tc_cnt + 1
                s_cnt  = -1
                for ci in range(0, ChNum):
                    for ti in range(0, TimeSampleNum):
                        for fi in range(0, FrqSampleNum):
                            s_cnt = s_cnt + 1
                            Data[tc_cnt, s_cnt] = OriginData[k][ci, fi, ti, tryi]
                            Label[tc_cnt] = l
        return Data, Label
#----------------------------------------------------------------------------
def ShapeDictTo2D(OriginDict, *, LabelDict, DataDimNum, TrialNum):
    #クラス数を確認
    ClassNum = len(OriginDict)
    #ラベル配列
    Label = np.zeros([TrialNum*ClassNum])

    #2次元データ配列作成
    Data = np.zeros([TrialNum*ClassNum, DataDimNum])
    tc_cnt = -1
    for k, l in LabelDict.items():
        for tryi in range(0, TrialNum):
            tc_cnt = tc_cnt + 1
            Data[tc_cnt, :] = OriginDict[k][:, tryi]
            Label[tc_cnt] = l
    return Data, Label

#----------------------------------------------------------------------------
