import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
ROOTPATH = PYPATH + "./../../../../main/"
sys.path.append(ROOTPATH)

from common_modules.ext.kagenomoheji.img_similar import compare_color_histgrams

score_similar = compare_color_histgrams(
    path_base_img = ROOTPATH + "/images/test/gettyimages-1194679097.jpg",
    path_comp_img = ROOTPATH + "/images/test/gettyimages-1194679097_grayscale.jpg",
    resize = (200, 200),
    display_histgrams = True
)
print(score_similar)

