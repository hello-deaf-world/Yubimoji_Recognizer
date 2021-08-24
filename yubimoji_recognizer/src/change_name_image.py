from ja_dict import ja_dict
from color import Color
import os
import glob
import shutil
import datetime


# To store new images need to rename to name of Hiragana and "NO.png"


def main():

    imagesList = getImages()
    afterList = changeName(imagesList)


    if filemove(afterList):
        print("successed to move the file to each folders")

    addId()

    


# it can get the image all in the images file
def getImages():

    imagesList = glob.glob("images//new_images//*.png" )
    return imagesList

# it can change image's name to "a_(number)_(0= didn't recognize, 1= did recognize)_datatime.png"
def changeName(images):

    # it add to "filenameList","pathnameList" if there is '_NO' to "filename"
    # and it pick 'pickedfilename' from 'filename'.
    filenameList = []
    pathnameList = []
    beforenameList = []
    for filename in images:
        if "NO.png" in filename :
            pickedfilename = os.path.basename(filename)
            filenameList.append(pickedfilename)

            #it add "pathname" to "pathnameList"
            pathname = filename.replace(pickedfilename, '')
            pathnameList.append(pathname)

            beforenameList.append(filename)

    if len(filenameList) != len(pathnameList):
        return print(Color.RED + "Error: It is different the number of files in filenameList and pathnameList." + Color.END)

    else:
        # it change New name to aftername from beforename
        newfilenameList = []
        for image in filenameList:
            for ja_dict_key in ja_dict.values():
                if ja_dict_key in image and "NO.png" in image:

                    image = "{name}_0_{datetime}.png".format(
                        name = ja_dict_key, datetime = get_current_yyyymmdd()
                        )

                    newfilenameList.append(image)

    newnameList = []
    for i in range(len(newfilenameList)):
        newname = pathnameList[i] + newfilenameList[i]
        newnameList.append(newname)


    # return  beforenameList, newnameList

    if len(beforenameList) == len(newnameList):
        print(Color.PURPLE + "beforeList :" + str(beforenameList)+ Color.END)
        print(Color.RED + "afterList :" + str(newnameList)+ Color.END)

        afterList = []
        for before , after in zip(beforenameList, newnameList):
            
            if not os.path.exists(after):
                os.rename(before, after)
                afterList.append(after)

            else:
                copycount = 0
                while True:
                    afterfind = after.find('.png')
                    after = after[:afterfind] + '_' + str(copycount)+ '_' + after[afterfind:]
                    if not os.path.exists(after):
                        os.rename(before, after)
                        afterList.append(after)
                        break
                    else:
                        copycount += 1

        print(Color.GREEN +'Successed to change the images name'+ Color.END)
        return afterList


            # print("changed name : "+ str(os.path))
# it can move the image data to each label's folders
def filemove(filepathList):


    

    for filepath in filepathList:
        filename = os.path.basename(filepath)
        file_idx = filename.find("_")

        count = 0
        for en in ja_dict.values():
            if filename[:file_idx] == en:
                movepath =  "images//{count}_{en}//".format(count=count, en=en) 
                shutil.move(filepath,movepath)
                print('move before:' ,filepath ," ", "move after", movepath)
            else:
                count += 1


def addId():
    
    ja_count = 0

    for ja in ja_dict.values():
        dir = 'images//{idx}_{ja}'.format(idx=ja_count,ja=ja)
        os.path.exists("{dir}//*.png".format(dir=dir))
        images = glob.glob("{dir}//*.png".format(dir=dir))
        if 0 == len(images):
            continue
        else:
            numberOfImage = len(images)
        # print(images)
        
        todayfileList = []
        for file in images:
            current = get_current_yyyymmdd()
            filename = '{ja}_0_{current}'.format(ja=ja, current= current)
            # print(filename)
            if filename in file:
                
                todayfileList.append(file)

        if not todayfileList:
            continue
    
        numberOfTodayfile = len(todayfileList)

        # print(todayfileList)

        fromthispoint = abs(numberOfImage - numberOfTodayfile)
        addIdfileList = []
        for file in todayfileList:
            filename = os.path.basename(file)
            idxfound = filename.find('_')
            addIdfile = filename[:idxfound+1] + str(fromthispoint) + '_0_' + current
            addIdfileList.append(addIdfile)
            fromthispoint += 1

        # print(Color.GREEN + str(addIdfileList) + Color.END)
        for before, after in zip(todayfileList,addIdfileList):
            afterpath = "images//{idx}_{ja}//{after}.png".format(idx=ja_count,ja=ja,after=after)

            if afterpath:
                os.rename(before, afterpath)
                print(Color.PURPLE + before + Color.END,"->",Color.GREEN + afterpath + Color.END)
            else:
                return print(Color.RED + "can't add the Id -> ",str(before) +Color.END)
        
        ja_count += 1

    print(Color.GREEN + "successed to add the Id to each files in each folders" + Color.END)


def get_current_yyyymmdd():
    
    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y%m%d')

    return yyyymmdd


# addId()

main()


     
