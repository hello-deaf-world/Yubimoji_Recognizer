import csv
import datetime

logFile = 'log.csv'

def inputLog(logfile, id, id_in_label, label_ja, label_en, file_dir, left_or_hand, ):

    # open the input_log_csv_file.py
    with open( logfile , 'a', encoding= 'utf-8', newline = '') as f:

        logList = []
        logList.append(todayDate()) 
        logList.append()




        writer = csv.writer(f)
        writer.writerow( --- )









