import csv

filename = "yubimoji_data.csv"

#指文字データをcsvに入れる
def inputDate(JaHira_label,JaLo_label, hand_label, hand_landmarks):

    with open(filename, 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([JaHira_label ,JaLo_label , hand_label , hand_landmarks])