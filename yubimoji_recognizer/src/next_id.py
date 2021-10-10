from color import Color
import sys


def get_next_id():
    '''
    (杉村)next_id.txtでidの取得/新規idの登録の試験するってこと？
    '''
    file = "next_id.txt"
    with open(file, "r",encoding="utf-8") as f:
        data = f.read()
        if "次回の画像id番号" in data:
            findData = data.find("次回の画像id番号: ") + 11
            #次回のidを取得
            id_number = int(data[findData:])
        else:
            print(Color.RED + "次回の画像id番号を確認できませんでした。" + Color.END)
            sys.exit()        
        
    with open(file,"w",encoding="utf-8")as f:
        f.write("次回の画像id番号: {}".format(id_number + 1))


    return str(id_number)
