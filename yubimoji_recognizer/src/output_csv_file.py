import csv 
import os
import pandas as pd

#csv data 
#forid_fromscore_List = id, create_date, id_in_label, label_ja, label_en, file_dir, left_or_right_label, left_or_right_score
#Pass data as two list types

#class_data後で引数名変える


self.id = id
self.create_date = create_date
self.id_label = id_label
self.label_en = label_en
self.label_ja = label_ja
self.filedir = filedir
self.left_or_right_label = left_or_right_label
self.left_or_right_score = left_or_right_score
self.landmarks_list = landmarks_list
        





def extract_object(data_recognize_hand):
    # クラスからクラス内変数(フィールド，プロパティ等言い方いろいろ)のデータを取得する関数？
    # いる・・・？

    # どんな引数・戻り値の，どんな処理をする関数の組み合わせが必要かの簡単な設計が必要かもね～
    
    # ここの左辺でクソ長いインスタンス名＋フィールド名を書いて読みやすくってこと？
    # 杉村がイメージしていたのは，output_csv()の引数がインスタンス
    # 俺もそのイメージやったけど、この関数があるのをみて、
    
    id = data_recognize_hand.id
    id_in_label = data_recognize_hand.id_in_label
    landmark_x = data_recognize_hand.landmark

    return output_csv(for_id_from_score_List, landmarks_List)

# まじで、違うの
# (杉村)サブクラスを作る際の１手法が継承
# (杉村)クラスのオブジェクト(変数)を作るのはインスタンス化，かな．今はこっちの話？
# for_id_from_score_List,landmarks_List

# dataRecognizeHand_obj = クラスからインスタンス化したオブジェクト
# dataRecognizeHand_obj.id
# dataRecognizeHand_obj.create_date

def output_csv(obj: DataRecognizeHand):
    # 近代pythonでは型の表記だけできる…(厳密な型判定はしてくれない)
    # 静的型付けは，コード書いてる・コンパイルする時点でエラー教えてくれるから嬉しいところ．
    # pythonは(javascriptも？)動的型付けだから引数にstr/int/オブジェクトなんでもいれてしまえる
    # 実行して初めてエラーが出てわかる

    # javascriptもだね．最近は代替jsがでてきてtypescriptとか軽めの静的型付できるようにしようという動きはある

    # (補足すると)objはわかりにくすぎるので，わかりやすくかつ短い変数名つける努力は必要

    # obj.id
    # obj.createdate

    # dataRecognizeHand_obj.id = idのデータ
    # dataRecognizeHand_obj.create_date = 画像を読み込んだdateデータ


def output_csv(dataRecognizeHand_obj):
    csvname = "hand_landmark_data.csv"
    with open (csvname , 'a' ,encoding = "utf-8") as f :
        #change pandas
        writer = csv.writer(f)

        
        landmarks_data = ""
        for hand_data_List in dataRecognizeHand_obj.landmarks_List :
            joined_hand_data = ','.join(map(str, hand_data_List))
            landmarks_data += "," + joined_hand_data 


        #list=>string cast
        #joined_landmarks=','.join(map(str, landmarks_List))
        setup_header(csvname, f)
        joined_for_id_from_score = ','.join(map(str, for_id_from_score_List))
        writer.writerow(joined_for_id_from_score, landmarks_data)
    
#header=True or False Branch
def setup_header(csvname,f) :
    #file exsist=True ot False
    if(os.path.exists(csvname)):
        lines = len(f.readlines())

        if lines < 1 :
            writer =  csv.writer(f)
            writer.writerow(create_header_name())
        #1行でも存在する場合、1番上の行のデータが何かを調べる
        else:
            df = pd.read_csv(csvname, encording="utf-8")
            #ヘッダー取得
            df.colums.values

            #取得したヘッダーのデータと元々のheader名が違う場合は書き直す（pandas）
            header_names = create_header_name()
            if set(df.colums.values) == set(header_names) :
                #リストの中の順番が変わっていても、header_nameと名前が同じなら通す
                df.colums.values == header_names   
                pass
            else:
                #同じではない→1行だけ書き直す処理（pandas）
                df.rename(columns = header_names)
                
                # 書き出す前にファイル名変更の形でバックアップ取る
                #新しいCSV書きだし
                

    #ファイルがない場合→ファイル作成＋ヘッダー追加
    # else :
    #     header_names = create_header_name() 
    #     df = pd.read_csv(csvname, names = [header_names], encording = "utf-8")


#ヘッダー名を作成、変更
def create_header_name() :
    headers_list = ["id","create_date","id_in_label","label_ja","label_en","file_dir","left_or_right_label","left_or_right_score"]
    
    #index0~21を作る
    index_number = ""
    for index in range(21):
        x = "index{index}_X".format(index = str(index))
        y = "index{index}_Y".format(index = str(index))
        z = "index{index}_Z".format(index = str(index))

        #ヘッダー名に追加,List=>list Ctrl+D
        headers_list.append(x)
        headers_list.append(y)
        headers_list.append(z)

        #index_number += ",{x},{y},{z}".format(x=x,y=y,z=z)

    return headers_list