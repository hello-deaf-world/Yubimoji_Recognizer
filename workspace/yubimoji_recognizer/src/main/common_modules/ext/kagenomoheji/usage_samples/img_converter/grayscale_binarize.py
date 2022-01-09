import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
ROOTPATH = PYPATH + "./../../../../.."
sys.path.append(ROOTPATH)

from common_modules.ext.kagenomoheji.img_converter import (
    selective_convert_img,
    ImgConvertMethod,
    CV2CvtColorMode,
    CV2ThresholdMode,
    CV2CvtGammaMode
)


'''
下記の処理を選択し順番に処理させるサンプル．
1. RGB色空間に戻す処理
2. グレースケール
3. (白黒に)2値化
'''
selective_convert_img(
    [
        {
            # cv2.imreadでBGRまたはBGRAと見なされてしまうので，まず戻す必要あり
            "method": ImgConvertMethod.CVTCOLOR,
            "params": {
                "mode": CV2CvtColorMode.BGR2RGB
            }
        },
        {
            "method": ImgConvertMethod.CVTCOLOR,
            "params": {
                "mode": CV2CvtColorMode.RGB2GRAY
            }
        },
        {
            "method": ImgConvertMethod.THRESHOLD,
            "params": {
                "mode": CV2ThresholdMode.BINARY,
                "threshold": 200
            }
        }
    ],
    path_img = ROOTPATH + "/images/test/gettyimages-1194679097.jpg",
    display_progress_imgs = True
)