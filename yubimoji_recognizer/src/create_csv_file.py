import csv
import glob
import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"


ROOT_PATH = PYPATH

#csvファイル指定
# filename = "D:\Hello_Deaf_World\pro-yubimoji-_recognizer\Github\Yubimoji_Recgnizer\yubimoji_recognizer\src\yubimoji_data.csv"


#CSV作成
def makeCSV(filename):
    hedder = ["Hiragana", "Romaji" , "hand_labels" , "hand_landmarks" ]
    

    with open(filename, 'w', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(hedder)

makeCSV('yubimoji_data.csv')


                

