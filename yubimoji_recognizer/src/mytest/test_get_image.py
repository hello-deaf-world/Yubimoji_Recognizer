# test_get_image.pyのほうがいい
# どの関数をてすとするかという意味

import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
ROOTPATH = PYPATH + "./.." # ここは，srcの階層に戻るための設定．OK．
sys.path.append(ROOTPATH)


from get_images import get_images


print(PYPATH)
imageList = get_images(ROOTPATH,"1")

print(imageList)