import csv

def outputcsv(id, create_data, id_in_label, label_ja, label_en, file_dir, left_of_right,left_of_right_index, left_of_right_socore):

    with open('test.csv', 'a', encoding = 'utf-8') as f:
        writer = csv.writer(f)

        data = '{id},{create_data},{id_in_label},{label_ja},{label_en},{file_dir},{left_of_right},{left_of_right_index},{left_of_right_score}'.format(
            id, create_data, id_in_label, label_ja, label_en, file_dir, left_of_right,left_of_right_index, left_of_right_socore
        )


        writer.writerow(data)