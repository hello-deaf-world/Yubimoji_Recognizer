import os
import datetime
from ja_dict import ja_dict


# # This code is the function for yubimoji_recognize.py

# # it can to get the id
def get_id_data():

	csvname = 'test.csv'
	with open(csvname) as f:
		lines = len(f.readlines())
		return lines + 1


# yyyy-mm-dd
def get_current_yyyy_mm_dd():

    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y-%m-%d')

    return yyyymmdd

def get_id_label(file):

	filename = os.path.basename(file)
	count = 0
	for idx, i in enumerate(filename):
		if i == '_':
			count += 1
			if count == 2:
				findidx = idx
				break

	id_label = filename[:findidx]
	return id_label
	
	# print(id_label)

# it can to get the label_en from di_jact
def get_label_en(filepathName):

	filename = os.path.basename(filepathName)
	idx = filename.find('_')
	label_en = filename[:idx]
	return label_en

# it can to get the label_ja from di_jact
def get_label_ja(label_en):

	for key , value in ja_dict.items():
		if label_en == value:
			label_ja = key
			return label_ja

def get_current_dir(file):
    
	filediridx = file.find("images")
	filedir = file[filediridx:]
	return filedir

# it can to get the Handedness data(index, score, label)
def get_Handedness(data):


		for handData in data:
			for handlabel in handData.classification:
				# index = handlabel.index
				score = handlabel.score
				label = handlabel.label

		return score, label


def get_landmark(data):

	handDataList = []
	# landmark_data = ''
	for landmarks in data:
		for landmark in landmarks.landmark:
			x = landmark.x
			y = landmark.y
			z = landmark.z
			# landmark_data += ',{x},{y},{z}'.format(x = x, y = y, z = z)
			handDataList.append(x)
			handDataList.append(y)
			handDataList.append(z)

	return handDataList






# print(get_label_en("tabaka_buk_ajfa"))