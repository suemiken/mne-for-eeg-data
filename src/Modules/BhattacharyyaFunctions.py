# -*- coding: utf-8 -*-
import numpy as np
import math

def Bhattacharyya(H1, H2):
    Bd = 0
    for x in range(0, H1.shape[0]):
        Bd = Bd + np.sqrt(H1[x]*H2[x])
    Bd = -1*np.log2(Bd)
    return Bd

#------------------------------------------------------------------
def DictRange(Dict, IMax=0, Imin=0):
    Max = IMax
    min = Imin
    for k in Dict.keys():
        tmp = np.max(Dict[k])
        if tmp > Max:
            Max = tmp

        tmp = np.min(Dict[k])
        if tmp < min:
            min = tmp
    return (min, Max)

#--------------------------------------------------------
def CreateBdDataBase1(LenBd):
# バタチャリア距離計算結果格納配列を持つ辞書型「Bd」
# 配列の長さ = 全クラスから2クラスを選ぶ組み合わせ×チャネル数×周波数セクションの数×時間セクションの数(「LenBd」)
# Bd > {'val':np.array[double(バタチャリア距離の計算値(0<Bd値<1)), ...],
#       'ch':[int(チャネルインデックス), ...],(int型ね)
#       'FrqSectionのキー':['FrqSectionのキー', ...],
#       'TimeSectionのキー':['FrqSectionのキー', ...] }
    Bd = {'val':np.zeros([LenBd]),
          'ch':np.zeros([LenBd], dtype=np.int16),
          'fskey':[None for _ in range(LenBd)],
          'tskey':[None for _ in range(LenBd)]}
    return Bd

#--------------------------------------------------------
def CreateBdDataBase2(LenBd):
# バタチャリア距離計算結果格納配列を持つ辞書型「Bd」(バージョン2)
# 配列の長さ = 全クラスから2クラスを選ぶ組み合わせ×チャネル数×周波数セクションの数×時間セクションの数(「LenBd」)
# Bd > {'val':np.array[バタチャリア距離の計算値(0<Bd値<1), ...],
#       'ch':np.array[チャネル, ...], (int型ね)
#       'FrqSectionのキー':np.array[[始点インデックス, 終点インデックス], ...],  (int型ね)
#       'TimeSectionのキー':np.array[[始点インデックス, 終点インデックス], ...] } (int型ね)
    Bd = {'val':np.zeros([LenBd]),
          'ch':np.zeros([LenBd], dtype=np.int16),
          'fskey':np.zeros([LenBd, 2], dtype=np.int16),
          'tskey':np.zeros([LenBd, 2], dtype=np.int16)}
    return Bd
#---------------------------------------------------------
class BhattacharyyaDistanceDataBase:
    # MODE = 'ONLY_KEY' : 元データのインデックス情報だけ
    # MODE = 'KEY_AND_DATA' : 元データのインデックスに加えて元データも格納
    def __init__(self, DataBaseSize):
        self.nowindex = 0

        self.value = np.zeros([DataBaseSize])
        self.ch = np.zeros([DataBaseSize], dtype=np.int16)
        self.frqrange = np.zeros([DataBaseSize, 2], dtype=np.int16)
        self.timerange = np.zeros([DataBaseSize, 2], dtype=np.int16)

    def AppendData(self, value, ch, FrqRange, TimeRange):
        self.value[self.nowindex] = value
        self.ch[self.nowindex] = ch
        self.frqrange[self.nowindex] = FrqRange
        self.timerange[self.nowindex] = TimeRange

        self.nowindex = self.nowindex + 1

    def DescendingOrderSort(self):
        return self.value.argsort()[::-1]

        #self.value = self.value[i]
        #self.ch = self.ch[i]
        #self.frqrange = self.frqrange[i]
        #self.timerange = nself.timerange[i]

    def SearchFvData(self, Data, *, i): # i:index
        return Data[self.ch[i], self.frqrange[i][0]:self.frqrange[i][1],
                            self.timerange[i][0]:self.timerange[i][1]]

#--------------------------------------------------
class AnalysisDataBase:
    def __init__(self, DataBaseSize):
        exec("name%d = %d" % (n, 100 + n))


    def GetDictFormatByDB():
        Dict = 0


#----------------------------------------------------------
def SetBd(Bd, index):
    Bd['val'][cnt] = BF.Bhattacharyya(H1, H2) # バタチャリア距離(自作関数で)計算
    Bd['ch'][cnt] = ci
    Bd['fskey'][cnt] = np.array(fi).astype(int)
    Bd['tskey'][cnt] = np.array(ti).astype(int)
    return Bd
