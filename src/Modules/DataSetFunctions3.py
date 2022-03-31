# -*- coding: utf-8 -*-
import numpy as np
import copy
import sys

class KfoldCrossValidation:
    #-------------------------------------------------
    def __init__(self, foldnum, DataBase, trialaxis = 2):
        self.foldnum = foldnum #交差検証数
        self.OrgData = DataBase #元データ

        #トライアルの引数をインデックスに直す
        if type(trialaxis) is str:
            self.trialaxis = DataBase.Class[0].FindAxis(trialaxis)
            self.trialkey = trialaxis
        elif type(trialaxis) is int:
            self.trialaxis = trialaxis
            self.trialkey = DataBase.Class[0].FindKey(trialaxis)

        self.trialnum = DataBase.Class[0].shape[self.trialaxis] #トライアル数

        self.idx = np.random.choice(self.trialnum, self.trialnum, replace=False)
        #print(self.idx)
        #self.idx = np.arange(self.trialnum) # debug用(ランダムでない)
        self.split_idx = np.array_split(self.idx, self.foldnum, 0)
    #-------------------------------------------------
    def SplitTrainTest(self, foldi):
        test_idx = self.split_idx[foldi]
        train_idx = np.array([], dtype='int64')
        for oi in range(len(self.split_idx)):
            if oi != foldi:
                train_idx = np.append(train_idx, self.split_idx[oi])

        org_axiskeys = self.OrgData.Class[0].axiskeys #元の次元の並び順を保存
        tmp_axiskeys = [key for key in org_axiskeys if key != self.trialkey]
        tmp_axiskeys.insert(0, self.trialkey)
        self.OrgData.Transpose(tmp_axiskeys) #この順番に並び替え

        #テスト用、データ用のデータベース作成
        Data_test = DataBase()
        Data_train = DataBase()
        for CName in self.OrgData.ClassNames:
            i = self.OrgData.ClassNames.index(CName)

            Data_test.AddClassData(ClassName=CName, axiskeys=self.OrgData.Class[i].axiskeys,
                         data = self.OrgData.data(CName)[test_idx] )
            Data_train.AddClassData(ClassName=CName, axiskeys=self.OrgData.Class[i].axiskeys,
                         data = self.OrgData.data(CName)[train_idx] )

        Data_test.Transpose(org_axiskeys) #元の並び順に戻す
        Data_train.Transpose(org_axiskeys)
        self.OrgData.Transpose(org_axiskeys)

        return Data_test, Data_train
    #-------------------------------------------------
#===============================================================================
#===============================================================================
# データクラス
class DATA:
    #-------------------------------------------------
    def __init__(self, data, axiskeys):
        if data.ndim != len(axiskeys):
            print('dataの次元とaxiskeysの数が合いません。')
            sys.exit(1)

        self.axiskeys = axiskeys
        self.shape = data.shape
        self.data = data
        self.dim = data.ndim
    #-------------------------------------------------
    # キーを入力、axisを返す[OK]
    def FindAxis(self, key):
        if type(key) is str:
            return self.axiskeys.index(key)
        elif type(key) is list or type(key) is np.ndarray:
            return [list(self.axiskeys).index(k) for k in key]
    #-------------------------------------------------
    # axisを入力、キーを返す[OK]
    def FindKey(self, axis):
        if type(axis) is int:
            return self.axiskeys[axis]
        elif type(axis) is list or type(axis) is np.ndarray:
            return [self.axiskeys[ax] for ax in axis]
    #-------------------------------------------------
    # データの軸を任意の順番で入れ替え
    def Transpose(self, newaxis):
        try:
            # 新しくaxiskeysを更新するために、newaxisをすべてキーに
            for i, na in enumerate(newaxis):
                newaxis[i] = self.FindKey(na) if type(na) is int else na
        except TypeError as err:
            print('リスト型である必要があります。>', err)
            sys.exit(1)

        #ソートする順番のインデックを獲得(newaxisをすべてインデックスに)
        sort_idx = [self.FindAxis(na) for na in newaxis]
        #入れ替え作業
        self.axiskeys = [self.axiskeys[i] for i in sort_idx] #軸キー
        self.shape = tuple([self.shape[i] for i in sort_idx]) #確認用shape
        self.data = self.data.transpose(sort_idx) #データ
        self.dim = self.data.ndim

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
    def AxisLen(self, axis):
        if type(axis) is int:
            return self.shape[axis]
        elif type(axis) is str:
            return self.shape[self.FindAxis(axis)]

#===============================================================================
#===============================================================================
# データベースクラス
class DataBase:
    #-------------------------------------------------
    def __init__(self):
        self.Class = []

        self.ClassNames = []

        self.ClassLabel = []
        self.nextLabel = 0

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
    #指定した軸のサイズを返す
    def ClassAxisLen(self, ClassName, axis):
        if type(ClassName) is str:
            Classi = self.ClassNames.index(ClassName)
        elif type(ClassName) is int:
            # print(ClassName)
            Classi = ClassName

        return self.Class[Classi].AxisLen(axis)

    #-------------------------------------------------
    #参照関数
    def data(self, ClassName, index=None):
        if type(ClassName) is str:
            Classi = self.ClassNames.index(ClassName)
        elif type(ClassName) is int:
            Classi = ClassName

        if index == None:
            return self.Class[Classi].data
        elif type(index) is str:
            return self.Class[Classi].data[self.Class[Classi].FindAxis(index)]
        else:
            return self.Class[Classi].data[index]
    #-------------------------------------------------
    #データの軸入れ替え
    def Transpose(self, axis):
        for i in range(self.ClassNum):
            self.Class[i].Transpose(axis)
    #-------------------------------------------------
#===============================================================================
#===============================================================================
class ShapeDataBase:
    def __init__(self, OrgData, trialaxis=2, shape_mode='1D', shuffle=False):
        CLS = OrgData.ClassNames #クラスキーを獲得
        # trialaxisとtrialkeyを準備
        if type(trialaxis) is str:
            self.trialaxis = OrgData.Class[0].FindAxis(trialaxis)
            self.trialkey = trialaxis
        elif type(trialaxis) is int:
            self.trialaxis = trialaxis
            self.trialkey = OrgData.Class[0].FindKey(trialaxis)

        # 軸の入れ替え(トライアルaxisを0に持ってくる)
        org_axiskeys = OrgData.Class[0].axiskeys #元の次元の並び順を保存
        new_axiskeys = [key for key in org_axiskeys if key != self.trialkey]
        new_axiskeys.insert(0, self.trialkey)
        OrgData.Transpose(new_axiskeys) #この順番に並び替え


        #2Dモード(kerasのCNN用) +++++++++++++++++++++++++++++++++++++++++++++++
        if shape_mode == '2D':
            # 整形する際のデータのシェイプを作る
            dim_like = [0]
            for i in range(OrgData.data(0).ndim):
                if i != 0:
                    dim_like.append(OrgData.data(0).shape[i])
            shapedata = np.zeros(dim_like)# データ配列初期化
            self.Label = np.zeros([0])# ラベル配列初期化

            # データとラベル作成
            for i, cls in enumerate(CLS):
                trial_c = OrgData.data(cls).shape[0]
                shapedata = np.append(shapedata, OrgData.data(cls), axis=0) #データをアペンド
                self.Label = np.append(self.Label, np.full(trial_c, OrgData.ClassLabel[i])) #ラベルをアペンド
            self.stack = DATA(shapedata, new_axiskeys)

        #1Dモード(sklearnの分類器, kerasのNN用) ++++++++++++++++++++++++++++++++
        elif shape_mode == '1D':
            # 整形する際のデータのシェイプを作る
            dim_like = [0, 1]
            for i in range(OrgData.data(0).ndim):
                if i != 0:
                    dim_like[1] = dim_like[1] * OrgData.data(0).shape[i]
            shapedata = np.zeros(dim_like)# データ配列初期化
            self.Label = np.zeros([0])# ラベル配列初期化

            # データとラベル作成
            for i, cls in enumerate(CLS):
                trial_c = OrgData.data(cls).shape[0]
                shapedata = np.append(shapedata, OrgData.data(cls).reshape(trial_c, -1), axis=0) #データをアペンド
                self.Label = np.append(self.Label, np.full(trial_c, OrgData.ClassLabel[i])) #ラベルをアペンド
            self.stack = DATA(shapedata, [self.trialkey, 'Feature'])

        #トライアルの並びをランダムに
        if shuffle is True or ts == 1:
            idx = np.random.permutation(self.label().shape[0])
            self.stack.data = self.stack.data[idx, ...]
            self.Label = self.Label[idx]

        #OrgDataのみ元の順番に並び替え
        OrgData.Transpose(org_axiskeys)

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
