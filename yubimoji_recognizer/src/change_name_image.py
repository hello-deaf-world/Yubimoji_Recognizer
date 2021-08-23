from ja_dict import ja_dict
from function_get_current import get_current_yyyymmdd
import os
import glob

# To store new images need to rename to name of Hiragana and "NO.png"


def main():

    imagesList = getImages()
    beforeList, afterList = changeName(imagesList)

    if len(beforeList) == len(afterList):
        print("beforeList :" + str(beforeList))
        print("afterList :" + str(afterList))

        for before , after in zip(beforeList, afterList):
            os.rename(before, after)
            # print("changed name : "+ str(os.path))


    else:
        print(beforeList)
        print(afterList)
        print(
            "Error: It is different the number of files in beforeList and afterList."
            )


# it can get the image all in the images file
def getImages():

    imagesList = glob.glob("images//*//*.png" )
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

    print(filenameList)
    print(pathnameList)
    print(beforenameList)
    if len(filenameList) != len(pathnameList):
        return print("Error: It is different the number of files in filenameList and pathnameList.")

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


    return  beforenameList, newnameList



main()



