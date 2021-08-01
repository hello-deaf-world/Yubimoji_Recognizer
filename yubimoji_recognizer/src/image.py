#-----------------------------------------------------
# ここで杉村流の，このPythonファイルのカレントディレクトリの取得方法
import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
#-----------------------------------------------------
import glob

#読み込む写真のリスト
#読み込んだらコメントアウトすること

IMAGE_FILES = [

    # r"C:\Users\muray\Downloads/istockphoto-1078054462-170667a.jpg" # demo picture
    #---add---
    

]

def get_images(ROOT_PATH):
    DIR_NAME = "{root}/images".format(
        root = ROOT_PATH)
    
    # 上記ディレクトリにある画像ファイル群のファイル名リストを取得
    return glob.glob("{path}/*".format(path = DIR_NAME))

# 動作確認用
# get_images(PYPATH)
