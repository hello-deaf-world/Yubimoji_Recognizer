#-----------------------------------------------------
# ここで杉村流の，このPythonファイルのカレントディレクトリの取得方法
import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
#-----------------------------------------------------
import glob
import re



# 50音それぞれのフォルダを作成する
#---------------------------------------------

#---------------------------------------------


#読み込む写真のリスト
#読み込んだらコメントアウトすること

IMAGE_FILES = [

    # r"C:\Users\muray\Downloads/istockphoto-1078054462-170667a.jpg" # demo picture
    #---add---
    

]

def get_images(ROOT_PATH, key):
    
    # DIR_NAME = "{root}".format(
    #     root = ROOT_PATH)

    #上記ディレクトリにある画像ファイル群のファイル名リストを取得(拡張子.png)
    
    # True = picking only '0' | False = all of the images
    
    # (杉村)これが一般的かも．key_int = int try文にする
    
    print(ROOT_PATH)

    
    imagesList = []

    imagesList = glob.glob(ROOT_PATH + "//renamed_images//*//*.png")
    if key == "ALL":
        return imagesList
    

    try:
        key_int = int(key)
    except ValueError as e:
        raise e

    pick_imagesList = []
    if 0 <= key_int:    
        for p in imagesList:
            if re.search(r".+renamed_images\\.+\\.+_.+_{key}_.+\.png".format(key=key_int),p):
                pick_imagesList.append(p)

        return pick_imagesList       
    else:
        print("Error:0以上の自然数以外の数字データが入っています")
        sys.exit() 
            


    


