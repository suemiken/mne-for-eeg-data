# -*- coding: utf-8 -*-
import numpy as np
import copy
import sys

class KfoldCrossValidation:
    #-------------------------------------------------
    def __init__(self, K, DataBase, trialaxis = 2):
        self.K = K
        self.OrgData = DataBase

        if type(trialaxis) is str:
            self.trialaxis = np.where(DataBase.Class[0].axiskeys == trialaxis)[0][0]
        elif type(trialaxis) is int:
            self.trialaxis = trialaxis

        self.trialnum = DataBase.Class[0].shape[self.trialaxis]


        self.idx = np.random.choice(self.trialnum, self.trialnum, replace=False)
        #print(self.idx)
        #self.idx = np.arange(self.trialnum) # debug用(ランダムでない)
        self.split_idx = np.array_split(self.idx, self.K, 0)

    #-------------------------------------------------
    def SplitTrainTest(self, foldi):
        test_idx = self.split_idx[foldi]
        train_idx = np.array([], dtype='int64')
        for oi in range(len(self.split_idx)):
            if oi != foldi:
                train_idx = np.append(train_idx, self.split_idx[oi])

        index = np.arange(self.OrgData.Class[0].dim, dtype='int64')
        index = np.delete(index, self.trialaxis)
        index = np.insert(index, 0, self.trialaxis)
        self.OrgData.Transpose(axis=index)


        Data_test = DataBase()
        Data_train = DataBase()
        for CName in self.OrgData.ClassNames:
            i = self.OrgData.ClassNames.index(CName)

            Data_test.AddClassData( ClassName=CName, axiskeys=self.OrgData.Class[i].axiskeys,
                         data = self.OrgData.data(i)[test_idx] )
            Data_train.AddClassData( ClassName=CName, axiskeys=self.OrgData.Class[i].axiskeys,
                         data = self.OrgData.data(i)[train_idx] )


        index = np.arange(self.OrgData.Class[0].dim, dtype='int64')
        index = np.delete(index, 0)
        index = np.insert(index, self.trialaxis, 0)
        Data_test.Transpose(axis=index)
        Data_train.Transpose(axis=index)
        self.OrgData.Transpose(axis=index)

        return Data_test, Data_train
    #-------------------------------------------------
#===============================================================================
#===============================================================================
# データクラス
class DATA:
    #-------------------------------------------------
    def __init__(self, data, axiskeys):
        if data.ndim != np.array(axiskeys).shape[0]:
            print('dataの次元とaxiskeysの数が合いません。')
            sys.exit(1)


        self.data = data

        self.dim = data.ndim
        self.shape = data.shape

        self.axiskeys = np.array(axiskeys)
    #-------------------------------------------------
    def FixDATA(self, newdata, newaxiskeys=None):
        if self.dim != newdata.ndim and newaxiskeys==None:
            raise Exception('配列の次元が変わりました。新しく引数「axiskeys」を指定してください')
            sys.exit(1)

        self.data = newdata

        self.dim = newdata.ndim
        self.shape = newdata.shape

        if newaxiskeys != None:
            self.axiskeys = np.array(newaxiskeys)
    #-------------------------------------------------
    def DeleteDATA(self, deleteindex, axis=0):
        self.data = np.delete(self.data, deleteindex, axis=axis)

        self.dim = self.data.ndim
        self.shape = self.data.shape
    #-------------------------------------------------
    def axislen(self, axis):
        if type(axis) is int:
            return self.shape[axis]
        elif type(axis) is str:
            return self.shape[np.where(self.axiskeys == axis)[0][0]]

    #軸キーから軸インデックス取得　or　軸インデックスから軸キー取得
    def FindAxis(self, axis):
        if type(axis) is int:
            return self.axiskeys[axis]
        elif type(axis) is str:
            return np.where(self.axiskeys == axis)[0][0]

#===============================================================================
#===============================================================================
# データベースクラス
class DataBase:
    #-------------------------------------------------
    def __init__(self):
        self.Class = []

        self.ClassNames = []

        self.ClassLabel = []
        self.nextLabel = 1

        self.ClassNum = 0

    #-------------------------------------------------
    #データベース情報表示
    def info(self):
        print('=== DataBase Information =========')
        print(f'Class:{self.ClassNames}')
        print(f'Label:{self.ClassLabel}')
        print(f'ClassNum:{self.ClassNum}')
        print(f'DataShape -----------------------')
        for i in range(self.ClassNum):
            print(f'{self.ClassNames[i]}:(', end='')
            flag = 0
            for j in range(len(self.Class[i].axiskeys)):
                if flag == 0:
                    print(f'{self.Class[i].axiskeys[j]}={self.Class[i].data.shape[j]}', end='')
                    flag = 1
                else:
                    print(f', {self.Class[i].axiskeys[j]}={self.Class[i].data.shape[j]}', end='')
            else:
                print(')')
        print('----------------------------------')
        print('==================================')

    #-------------------------------------------------
    #クラス名変更
    def FixClassName(self, BeforeClassName, AfterClassName):
        Classi = self.ClassNames.index(BeforeClassName)

        self.ClassNemes[Classi] = AfterClassName

    #-------------------------------------------------
    #データ上書き
    def Fixdata(self, ClassName, data, axiskes=None):
        Classi = self.ClassNames.index(ClassName)

        self.Class[Classi].FixDATA(self, data, axiskeys)

    #-------------------------------------------------
    #クラスデータ追加
    def AddClassData(self, ClassName, axiskeys, data):
        self.Class.append(DATA(data, axiskeys))
        self.ClassNames.append(ClassName)

        self.ClassLabel.append(self.nextLabel)
        self.nextLabel = self.nextLabel + 1

        self.ClassNum = self.ClassNum + 1

    #-------------------------------------------------
    # クラスデータからデータ削除
    def ClassdataDelete(self, deleteindex, axis=0):
        for i in range(self.ClassNum):
            self.Class[i].DeleteDATA(deleteindex, axis=axis)

    #-------------------------------------------------
    #参照関数
    def data(self, ClassName, index=None):
        if type(ClassName) is str:
            Classi = self.ClassNames.index(ClassName)
        elif type(ClassName) is int:
            Classi = ClassName

        if index == None:
            return self.Class[Classi].data
        else:
            return self.Class[Classi].data[index]

    #-------------------------------------------------
    #指定した軸のサイズを返す
    def ClassAxisLen(self, ClassName, axis):
        if type(ClassName) is str:
            Classi = self.ClassNames.index(ClassName)
        elif type(ClassName) is int:
            print(ClassName)
            Classi = ClassName

        return self.Class[Classi].axislen(axis)

    #-------------------------------------------------
    #データの軸入れ替え
    def Transpose(self, axis=[]):
        for i in range(self.ClassNum):
            if len(axis) == 0:
                self.Class[i].data = self.Class[i].data.transpose()
                self.Class[i].axiskeys = self.Class[i].axiskeys[::-1]
            else:
                self.Class[i].data = self.Class[i].data.transpose(axis)
                self.Class[i].axiskeys = self.Class[i].axiskeys[axis]


            self.Class[i].shape = self.Class[i].data.shape
    #-------------------------------------------------

class ShapeDataBase:
    def __init__(self, OrgData, trialaxis = 2):

        if type(trialaxis) is str:
            self.trialaxis = OrgData.Class[0].FindAxis(trialaxis)
        else:
            self.trialaxis = trialaxis

        newfeaturenum = 1
        for di in range(OrgData.Class[0].dim):
            if di != self.trialaxis:
                newfeaturenum = newfeaturenum * OrgData.Class[0].shape[di]

        newtrialnum = 0
        for classi in OrgData.Class:
            newtrialnum = newtrialnum + classi.shape[self.trialaxis]


        shapedata = np.zeros([newtrialnum, newfeaturenum])
        self.Label = np.zeros([newtrialnum])


        index = np.arange(OrgData.Class[0].dim, dtype='int64')
        index = np.delete(index, self.trialaxis)
        index = np.insert(index, 0, self.trialaxis)
        OrgData.Transpose(axis=index)

        cnt = -1
        for ci in range(OrgData.ClassNum):
            for tryi in range(OrgData.data(ci).shape[0]):
                cnt = cnt + 1
                shapedata[cnt, :] = copy.deepcopy(OrgData.data(ci)[tryi].reshape(-1))
                # shapedata = np.append(shapedata, OrgData.data(ci)[tryi].reshape((0,-1)), axis=0) #使えないかも
                self.Label[cnt] = OrgData.ClassLabel[ci]

        index = np.arange(OrgData.Class[0].dim, dtype='int64')
        index = np.delete(index, 0)
        index = np.insert(index, self.trialaxis, 0)
        OrgData.Transpose(axis=index)

        self.stack = DATA(shapedata, ['Trial', 'Data'])

    #-------------------------------------------------
    #参照関数
    def data(self, index=None):
        if index == None:
            return self.stack.data
        else:
            return self.stack.data[index]
    
    def label(self):
        return self.Label
    #-------------------------------------------------
