from ja_dict import ja_dict
# from image import make_dir
import os


# ディレクトリを作成
# ja_dictから名前を取得
# ja_dictに追加するとその分追加ディレクトリを作成できる
def make_dir_renamed_images():
    
    count = 0
    for name in ja_dict.values():
        renamed_images_path = 'renamed_images\\{path}'.format(path= str(count) + "_" + name)
           
        os.makedirs(renamed_images_path,exist_ok=True)
        count += 1

        path = renamed_images_path + '\\' + name + '_memo.txt'
        
        if not os.path.exists(path):
            f = open(path,'w', encoding = 'utf-8')
            f.write('変更した'+ name + 'ラベルの画像データを格納しています。\n次回の画像id番号: 0')
            f.close()

def make_dir_new_images():

    count = 0
    for name in ja_dict.values():
        new_images_path = 'new_images\\{path}'.format(path= str(count) + "_" + name)

        os.makedirs(new_images_path, exist_ok=True)
        count += 1

        path = new_images_path + '\\' + name + '_memo.txt'

        if os.path.exists(path):
            pass
        else:
            with open(path, 'w', encoding = 'utf-8') as f:
                f.write('変更する前の'+ name + 'ラベルの画像データを格納しています。')


make_dir_renamed_images()
make_dir_new_images()
