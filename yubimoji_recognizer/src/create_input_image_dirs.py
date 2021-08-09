from Japanese_list import ja_list
# from image import make_dir
import os


# ディレクトリを作成
# ja_listから名前を取得
# ja_listに追加するとその分追加ディレクトリを作成できる
def make_dir():
    for i in range(len(ja_list)):
        path = 'images\\{path}'.format(path= str(i) + "." + ja_list[i])
        os.makedirs(path)

make_dir()