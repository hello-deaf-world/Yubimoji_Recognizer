import os
import datetime
from ja_dict import ja_dict
from function_get_current import get_current_yyyymmdd


# # This code is the function for yubimoji_recognize.py


def recognized_image_change_name(image):
    
	pickfilename = os.path.basename(image)
	dirname = os.path.dirname(image)

	count  = 0
	for idx,i in enumerate(pickfilename):
		if i == '_':
			count += 1
			if count == 2:
				changeidx = idx + 1
	
	if pickfilename[changeidx] == "0":
		s = list(pickfilename)
		s[changeidx] = '1'
		pickfilename = ''.join(s)
	
	findidx = pickfilename.find('.png')
	today = get_current_yyyymmdd()
	pickfilename = pickfilename[:findidx - 8] + today + pickfilename[findidx:]
    	
	new_image = dirname + "/" + pickfilename

	if os.path.exists(image):
		os.rename(image, new_image)

	return new_image

print(recognized_image_change_name("/renamed_images/0_a/a_0_0_20210904.png"))


    	
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