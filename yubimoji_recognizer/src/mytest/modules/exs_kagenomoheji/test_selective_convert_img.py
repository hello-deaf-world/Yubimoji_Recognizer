import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
ROOTPATH = PYPATH + "./../../.."
sys.path.append(ROOTPATH)

from modules.exs_kagenomoheji.img_converter import (
    selective_convert_img,
    ImgConvertMethod,
    CV2CvtColorMode,
    CV2ThresholdMode,
    CV2CvtGammaMode
)

selective_convert_img(
    [
        {
            # cv2.imreadでBGRまたはBGRAと見なされてしまうので，まず戻す必要あり(不要かも)
            "method": ImgConvertMethod.CVTCOLOR,
            "params": {
                "mode": CV2CvtColorMode.BGR2RGB
            }
        },
        # OK: SCALE/RESIZE/MOSAIC/CVTCOLOR/BLUR_AVG/BLUR_MED/BLUR_GAUSSIAN/BLUR_BILATERAL(激重)/INVERT/THRESHOLD/BGR_GAMMA_GRAY/BGR_SAT_BRT/DECOLOR/CVTGAMMA
        {
            "method": ImgConvertMethod.CVTCOLOR,
            "params": {
                "mode": CV2CvtColorMode.RGB2LUV
            }
        },
    ],
    path_img = ROOTPATH + "/images/test/gettyimages-1194679097.jpg",
    # path_result = ROOTPATH + "/images/test/gettyimages-1194679097_cvtcolor_rgb2luv.jpg",
    display_progress_imgs = True
)