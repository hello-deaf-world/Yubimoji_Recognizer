import cv2
import time

from ja_dict import ja_dict


device_id = 1
capture = cv2.VideoCapture(device_id)
name ="ren"

def job(name,index,ja):
    ret, frame = capture.read()
    fname1="new_images/" + str(index) + "_" + ja + "/" + ja + ".png"
    # fname2= #google drive

    cv2.imwrite(fname1,frame)
    # cv2.imwrite(fname2, frame)
    print(fname1 + " is created.")



for index, ja in enumerate(ja_dict.values()):
    print("「" + ja + "」をとります。")
    time.sleep(3)
    job(name,index, ja)
    
