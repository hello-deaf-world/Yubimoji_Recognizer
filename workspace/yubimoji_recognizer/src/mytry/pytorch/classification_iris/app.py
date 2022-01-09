import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
ROOTPATH = PYPATH + "."
sys.path.append(ROOTPATH)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import random_split, TensorDataset, DataLoader
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable


'''
- Refs
    - データ前処理
        - https://tanuhack.com/data-prep/
    - pytorch
        - https://yutaroogawa.github.io/pytorch_tutorials_jp/
        - iris分類/ワイン分類
            - https://rf00.hatenablog.com/entry/2018/05/13/180739
            - https://exture-ri.com/2021/01/04/pytorch-nn/
        - データセット
            - https://dreamer-uma.com/pytorch-dataset/
        - データセットの分割
            - https://qiita.com/takurooo/items/ba8c509eaab080e2752c
            - sklearn.model_selection.train_test_split()を併用する方法もあるらしい
        - Tensorの型
            - https://pytorch.org/docs/stable/tensors.html
                - dtypeと型クラスの対応表を確認できる
            - https://note.nkmk.me/python-pytorch-dtype-to/
                - torch.tensor()のdtypeで指定するやつら
            - 文字列型やっぱ無いんやな
    - pandas
        - 行・列の選択
            - https://note.nkmk.me/python-pandas-at-iat-loc-iloc/
            - https://stackoverflow.com/questions/16782323/python-pandas-keep-selected-column-as-dataframe-instead-of-series
    - seaborn
        - https://qiita.com/saira/items/31328921ad0a4c203db4
'''

# ディレクトリの用意
os.makedirs("{}outputs/".format(PYPATH), exist_ok = True)

# データセットの読み込み
fname = "{}datasets/iris-dataset.csv".format(PYPATH)
df_iris = pd.read_csv(
    fname,
    header = 0,
    sep = ",",
    encoding = "utf-8")

# 目的変数の数値エンコーディング
## tensorflow/torchのいずれにしても，目的変数を数値にしておいた方が処理しやすい
## OneHotEncode/HashEncode/Label(Ordinal)Encode/CountEncode/TargetEncodeなど…どの数値エンコーディングにすべきか？
### https://www.renom.jp/ja/notebooks/tutorial/preprocessing/category_encoding/notebook.html
### https://di-acc2.com/programming/python/3737/
### https://thefinance.jp/datascience/201109-2
#### カテゴリ間の大小関係とかが無い文字列のカテゴリ変数の数値エンコードは，LabelEncodeが一番楽そうだよな
df_iris["label_species"] = df_iris["species"].astype("category").cat.codes
# print(df_iris.head())

# 目的変数に基づく散布図行列で可視化
# sns \
#     .pairplot(df_iris, hue = "species") \
#     .savefig("{}outputs/pairplot.png".format(PYPATH))
# plt.show() # 表示されなくね？

# 説明変数と目的変数へデータ分割
## 目的変数は数値型であるべし
np_X = np.array(df_iris.loc[:, [col not in ["species", "label_species"] for col in df_iris.columns]])
np_y = np.array(df_iris.loc[:, ["label_species"]])
# for _x, _y in zip(np_X, np_y):
#     print(_x, _y)
# print(np_X.shape, np_y.shape)
# print(np_X.size, np_y.size)
# print(len(np_X), len(np_y))

# 説明変数・目的変数を学習データ・検証データに分割してDatasetに変換
## 訓練データ・検証データ・テストデータ
### 訓練データ・検証データは，訓練用のデータから用意しており，内訳を変えて再訓練する場合がある．
### テストデータは訓練済みモデルに渡す全く未知のデータ．
ratio_train = 0.8
##========================================================================
## (1)sklearn.model_selection.train_test_split()でデータ分割してからDatasetに変換する方法
'''
np_X_train, np_X_val, np_y_train, np_y_val = train_test_split(
    np_X, np_y,
    test_size = 1 - ratio_train,
    random_state = 71)
ds_train = TensorDataset(
    torch.tensor(np_X_train, dtype = torch.float),
    torch.tensor(np_y_train, dtype = torch.int))
ds_val = TensorDataset(
    torch.tensor(np_X_val, dtype = torch.float),
    torch.tensor(np_y_val, dtype = torch.int))
# for _x, _y in ds_train:
#     print(_x, _y)
'''
##------------------------------------------------------------------------
## (2)Datasetに変換してからtorch.utils.data.random_split()でデータ分割する方法
# ds = TensorDataset( # (2-1-1)以下2つの書き方は同じ
#     torch.FloatTensor(np_X),
#     torch.IntTensor(np_y))
ds = TensorDataset( # (2-1-2)
    torch.tensor(np_X, dtype = torch.float),
    torch.tensor(np_y, dtype = torch.int))
# for _d in ds:
#     print(_d)
# print(ds)
# print(len(ds))
len_train = int(len(ds) * ratio_train)
ds_train, ds_val = random_split(ds, [len_train, len(ds) - len_train])
# for _x, _y in ds_train:
#     print(_x, _y)
##========================================================================


# ミニバッチ訓練
##========================================================================
## (1)DataLoaderを用いる方法
### DataLoaderにDatasetを適用してミニバッチ対応
#### Epoch数とBatchSizeて別物なんだっけ
##### https://arakan-pgm-ai.hatenablog.com/entry/2017/09/03/080000
##### https://qiita.com/kenta1984/items/bad75a37d552510e4682
##### https://colab.research.google.com/github/YutaroOgawa/pytorch_tutorials_jp/blob/main/notebook/0_Learn%20the%20Basics/0_2_data_tutorial_jp.ipynb#scrollTo=8K9esMdhoH4x
dl_train = DataLoader(ds_train, batch_size = 10, shuffle = True)
dl_val = DataLoader(ds_val, batch_size = 10, shuffle = True)

### 訓練モデルの定義
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        # fc1: 入力=説明変数の4つ / 出力=100
        self.fc1 = nn.Linear(4, 100)
        # fc2: 入力=fc1の出力 / 出力=50
        self.fc2 = nn.Linear(100, 50)
        # fc3: 入力=fc2の出力 / 出力=目的変数の3つ
        self.fc3 = nn.Linear(50, 3)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim = 1)
model = Model()
print(model)

##------------------------------------------------------------------------
## (2)DataLoaderを用いない方法
##========================================================================



'''
色々メモ
- 手首から各landmarkへの相対座標を再計算すれば，回転を吸収した類似度の計算できるのでは？
    - 類似度も，順序の入れ替えではなくランドマーク別の乖離の総合評価で算出できれば良い
'''