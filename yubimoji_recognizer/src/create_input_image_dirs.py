from ja_dict import ja_dict
# from image import make_dir
import os


# ディレクトリを作成
# ja_listから名前を取得
# ja_listに追加するとその分追加ディレクトリを作成できる
def make_dir():
    count = 0
    for name in ja_dict.values():
        path = 'images\\{path}'.format(path= str(count) + "." + name)
        
        os.makedirs(path)
        count += 1
        

make_dir()