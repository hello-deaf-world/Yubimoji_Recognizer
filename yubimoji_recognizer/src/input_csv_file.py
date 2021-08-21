import csv

filename = "yubimoji_data.csv"

#指文字データをcsvに入れる
def inputDate(id,create_date,id_in_label,label_ja,label,en, file_dir, left_or_right, left_or_right_score, index0,,JaLo_label, hand_label, hand_landmarks):

    with open(filename, 'a', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([JaHira_label ,JaLo_label , hand_label , hand_landmarks])

