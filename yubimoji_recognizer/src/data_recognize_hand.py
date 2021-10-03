

class DataRecognizeHand:

    def __init__(self,id,create_date,id_label,label_en,label_ja,filedir,left_or_right_label,left_or_right_score,landmarks_list):

        
        self.id = id
        self.create_date = create_date
        self.id_label = id_label
        self.label_en = label_en
        self.label_ja = label_ja
        self.filedir = filedir
        self.left_or_right_label = left_or_right_label
        self.left_or_right_score = left_or_right_score
        self.landmarks_list = landmarks_list