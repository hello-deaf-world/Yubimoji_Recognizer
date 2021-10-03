import csv 
import os
import pandas as pd

#csv data 
#forid_fromscore_List = id, create_date, id_in_label, label_ja, label_en, file_dir, left_or_right_label, left_or_right_score
#Pass data as two list types

#class_data後で引数名変える




# def extract_object(data_recognize_hand):
   
#     dataRecognizeHand_obj = ""

#     return output_csv(dataRecognizeHand_obj.id,dataRecognizeHand_obj.create_date,dataRecognizeHand_obj.id_label,dataRecognizeHand_obj.label.en,dataRecognizeHand_obj.label_ja,dataRecognizeHand_obj.filedir,dataRecognizeHand_obj.left_or_right_label,
#     dataRecognizeHand_obj.left_or_right_score,dataRecognizeHand_obj.landmarks_list)



def output_csv(data_recognize_hand):

    prefolder = '作りたいフォルダまでのパス//作りたいフォルダ名'
    newfolder = prefolder
    csvname = "hand_landmark_data.csv"

    with open(csvname, "a", encording = "utf-8") as f :
        writer = csv.writer(f) 

        #csvファイルがあれば、認識したデータを書きだす処理だけ
        #無かったら、ヘッダーを書き出し、その後に認識データを書き出す
        if os.path.exists(prefolder) == True:
            # os.makedirs(newfolder + '//1', exsist_ok = True)
            # # shutil.copy2('コピーしたいファイルまでのパス',newfolder + 'コピーするファイルの名前')
            pass
        
        else:
            writer.writerow(create_header_name())
            
        writer.writerow(recognize_data_output(data_recognize_hand))


# self.id = id
# self.create_date = create_date
# self.id_label = id_label
# self.label_en = label_en
# self.label_ja = label_ja
# self.filedir = filedir
# self.left_or_right_label = left_or_right_label
# self.left_or_right_score = left_or_right_score
# self.landmarks_list = landmarks_list
    



#認識したデータを書き出すために整理
def recognize_data_output(data_recognize_hand):
    
    dr = data_recognize_hand
    recognize_data = "{},{},{},{},{},{},{},{}".format(dr.id,dr.create_data,dr.id_label,dr.label_en,dr.label_ja,dr.filedir,dr.left_or_right_label,dr.left_or_right_score)


    #ランドマークのデータを整理
    landmarks_data = ""
    #list=>string cast
    for hand_data_List in dr.landmarks_list :
        joined_hand_data = ','.join(map(str, hand_data_List))
        landmarks_data += "," + joined_hand_data 

    recognize_data += landmarks_data

    return recognize_data

    # setup_header(csvname)
    # joined_for_id_from_score = ','.join(map(str, for_id_from_score_List))
    # pd.to_csv(joined_for_id_from_score, landmarks_data)
    

#ヘッダー名を作成、変更
def create_header_name() :
    
    # headers_list = ["id","create_date","id_in_label","label_ja","label_en","file_dir","left_or_right_label","left_or_right_score"]
    headers_string = "id,create_date,id_in_label,label_ja,label_en,file_dir,left_or_right_label,left_or_right_score"
    
    #index0~21を作る
    for index in range(21):
        x = "index{index}_X".format(index = str(index)) #index0_X
        y = "index{index}_Y".format(index = str(index)) #index0_Y
        z = "index{index}_Z".format(index = str(index)) #index0_Z

        #ヘッダー名に追加（文字列型の場合）
        headers_string += "," +x+","+y+","+z    #,index0_x,index0_Y,index0_Z

        #ヘッダー名に追加,List=>list Ctrl+D (リスト型の場合)
        # headers_list.append(x)
        # headers_list.append(y)
        # headers_list.append(z)

        #index_number += ",{x},{y},{z}".format(x=x,y=y,z=z)
    
    #文字列の状態で返す    
    return headers_string


