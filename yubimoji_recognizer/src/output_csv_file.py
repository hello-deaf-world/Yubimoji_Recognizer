import csv 
import os
import pandas as pd

# Read CSV,get data each row
# def readcsv():
#     csvname = 
#     with open(csvname , 'r') as f:
#         reader = csv.reader(f)   
#         for row in reader:
#             print(row)
#         f.close()

# Write or postscript lines in csv file
#def outputcsv():
   # csvname = 
    #with open (csvname , 'w') as f :
       # writer = csv.writer(f)
        #writer.writerow()

#csv data 
#forid_fromscore_List = id, create_date, id_in_label, label_ja, label_en, file_dir, left_or_right_label, left_or_right_score
#Pass data as two list types

#class_data後で引数名変える
def extract_class(class_data):
  id = class_data.id
  id_in_label = class_data.id_in_label
  landmark_x = class_data.landmarks.x

def output_csv(for_id_from_score_List,landmarks_List):
    csvname = "hand_landmark_data.csv"
    with open (csvname , 'a' ,encoding = "utf-8") as f :
        #change pandas
        writer = csv.writer(f)
        
        #Extract from 2D list
        # for row in range(len(landmarks_List)) :
        #     for col in range(len(landmarks_List)):
        #         print(landmarks_List[row][col])
        
        landmarks_data = ""
        for hand_data_List in landmarks_List :
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
            #1番上の行を取得
        #取得した0行目のデータのheaderとheader名が違う場合は書き直す（pandas）
            if:
                #header_nameと同じ場合は
                pass
            else:
                #同じではない→1行だけ書き直す処理（pandas）

    #ファイルがない場合→ファイル作成＋ヘッダー追加
    else :
    header_names = create_header_name() 
    df = pd.read_csv(csvname, names = [header_names], encording = "utf-8")

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