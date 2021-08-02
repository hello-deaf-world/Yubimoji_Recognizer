#-----------------------------------------------------
# ここで杉村流の，このPythonファイルのカレントディレクトリの取得方法
import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
#-----------------------------------------------------
import glob

# 50音それぞれのフォルダを作成する
#---------------------------------------------
from Japanese_list import ja_list
#---------------------------------------------


#読み込む写真のリスト
#読み込んだらコメントアウトすること

IMAGE_FILES = [

    # r"C:\Users\muray\Downloads/istockphoto-1078054462-170667a.jpg" # demo picture
    #---add---
    

]

def get_images(ROOT_PATH):

    pathList = []

    DIR_NAME = "{root}".format(
        root = ROOT_PATH, )

    #上記ディレクトリにある画像ファイル群のファイル名リストを取得
    for i in range(len(ja_list)):
        files = glob.glob(ROOT_PATH + "images/" + str(i)+"."+ja_list[i]+"/*")
        #ディレクトリをpathListに追加
        for file in files:
            pathList.append(file)

    return pathList
            
            

            # test print -> succsess
            # print(file)

    # DIR_NAME = "{root}/images//0.a".format(
    #     root = ROOT_PATH, )
        
    #     #上記ディレクトリにある画像ファイル群のファイル名リストを取得
    # return glob.glob("{path}/*".format(path = DIR_NAME))

# 動作確認用
# print(get_images(PYPATH))

# ディレクトリを作成
# ja_listから名前を取得
# ja_listに追加するとその分追加ディレクトリを作成できる
def make_dir():
    for i in range(len(ja_list)):
        path = 'images\\{path}'.format(path= str(i) + "." + ja_list[i])
        
        if check_dir(path) == False: os.mkdir(path)
        continue

# ファイル名がかぶっていたらFalse かぶってなかったらTrueを返す
def check_dir(path):
    return os.path.isdir(path)

#ディレクトリ作成実行
#↓↓↓実行するときはコメント外す↓↓
# make_dir()

