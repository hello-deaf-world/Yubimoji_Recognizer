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

#---------------------------------------------


#読み込む写真のリスト
#読み込んだらコメントアウトすること

IMAGE_FILES = [

    # r"C:\Users\muray\Downloads/istockphoto-1078054462-170667a.jpg" # demo picture
    #---add---
    

]

def get_images(ROOT_PATH):
    
    DIR_NAME = "{root}".format(
        root = ROOT_PATH)

    #上記ディレクトリにある画像ファイル群のファイル名リストを取得(拡張子.png)
    
    images = glob.glob(ROOT_PATH + "renamed_images//*//*.png")
    return images
            

# 動作確認用
# print(get_images(PYPATH))



