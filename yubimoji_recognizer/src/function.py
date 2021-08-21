import datetime


# # This code is the function for yubimoji_recognize.py

# # it can to get the id
def getId():
    
	csvname = 'yubimoji_data.csv'
	with open(csvname) as f:
		totalRows = sum(1 for line in f)
		currentRows = totalRows + 1
		return currentRows
		
# # It can get a the execution's time 
# def getToday():
    
	getToday = datetime.date.today()
	return getToday

# # it can get to recognize 'R' or 'L' form data

def getRorL(data):
    
	for i in data:
    	data = i
	print(data)
	# print(data)
	# if "Right" in data and "index: 1" in data:
    # 		return 'Right'

	# elif "Left" in data and "index: 0" in data:
	# 	return 'Left'
	
	# else: return 'None'



# def getRorLScore(data):
    	
	
# def getIdInLabel():
