'''
グレースケールやRGBなどの処理の順番と引数を指定して，その順番どおりに画像変換を実行するコード

1. 渡された処理名(順序付き)一覧に対し，存在しない処理名が無いかチェック
2. ループの中に処理名の文字列に応じて全処理が分岐される形にし，処理名一覧を回す
'''
from enum import Enum
import traceback
from copy import deepcopy
import base64
import numpy as np
import cv2
import matplotlib.pyplot  as plt

def selective_convert_img(
    converters,
    path_img = None,
    np_img = None,
    path_result = None,
    display_progress_imgs = False):
    '''
    選択的かつ順序的にCV2による画像変換を実行できる関数．
    変換元はpath_imgの画像ファイルのパスでもnp_imgの読み込んでnumpy配列にした変数でも良い．
    変換後は基本numpy配列を返し，path_resultを指定すれば画像ファイル出力する．

    - Args
        - converters:[{"method":ImgConvertMethod, "params":dict}]:
            - ImgConvertMethod.SCALE: 縦横比固定での拡縮
                - ratio:float:
            - ImgConvertMethod.RESIZE: 幅・高さを指定してのリサイズ
                - width:int:
                - height:int:
            - ImgConvertMethod.CVTCOLOR: 色空間の変換
                - mode:CV2CvtColorMode:
            - ImgConvertMethod.BLUR_AVG: 平均フィルタによる平滑化
                - width:int: 
                - height:int: 
            - ImgConvertMethod.BLUR_MED: 中央値フィルタによる平滑化
                - size:int: 奇数
            - ImgConvertMethod.BLUR_GAUSSIAN: ガウシアンフィルタによる平滑化
                - width:int: 奇数
                - height:int: 奇数
                - sigma_x:int: 0の場合，自動計算らしい
            - ImgConvertMethod.BLUR_BILATERAL: バイラテラルフィルタによる平滑化
                - size:int:
                - sigma_color:int: 
                - sigma_space:int:
            - ImgConvertMethod.INVERT: 反転
            - ImgConvertMethod.THRESHOLD: 2値化
                - mode:CV2ThresholdMode:
                - threshold:int: 2値化の閾値
            - ImgConvertMethod.BGR_SAT_BRT: BGR色空間を入力とした彩度・明度補正
                - ratio_sat:float: 彩度の比率
                - ratio_brt:float: 明度の比率
            - ImgConvertMethod.BGR_GAMMA_GRAY: ret_uint8=Falseの場合に低輝度を潰さないグレースケールをしてくれる感
                - ret_uint8:bool: np.uint8で返すか
            - ImgConvertMethod.CVTGAMMA: ガンマ補正
                - mode:CV2CvtGammaMode:
                - gamma:float:
            - ImgConvertMethod.DECOLOR: 退色処理
            - ImgConvertMethod.MOSAIC: モザイク
                - ratio:float: モザイクの粒度．1未満．0に近いほど粒度が大きくなる．
        - path_img:str: 画像ファイルのパス
        - np_img:np.array: np.arrayとして読み込み済みの画像データ
        - path_result:str: 変換後の画像の保存先のパス
        - display_progress_imgs:bool: 変換過程の画像を可視化するか
    - Returns:
        - frame:np.array: 変換後のnp.arrayの画像データ
    '''
    methods = [c["method"] for c in converters]
    diff_methods = set(methods) - set(ImgConvertMethod.members())
    if len(diff_methods) > 0:
        raise KeyError("Cannot run because of including invalid converter.")
    
    frame = None
    if (frame is None) and (path_img is not None):
        frame = cv2.imread(path_img)
    if (frame is None) and (np_img is not None):
        frame = deepcopy(np_img)
    if frame is None:
        raise ValueError("Empty in variable 'frame'.")

    base_frame = deepcopy(frame)
    for conv_i, converter in enumerate(converters):
        # print(frame.shape)
        # print(frame)
        if converter["method"] == ImgConvertMethod.SCALE:
            '''
            縦横比固定で拡縮．
            '''
            frame = cv2.resize(
                frame,
                dsize = None,
                fx = converter["params"]["ratio"],
                fy = converter["params"]["ratio"])
        if converter["method"] == ImgConvertMethod.RESIZE:
            '''
            指定幅・高さにリサイズ．
            '''
            frame = cv2.resize(
                frame,
                dsize = (
                    converter["params"]["width"],
                    converter["params"]["height"]
                ))
        if converter["method"] == ImgConvertMethod.CVTCOLOR:
            '''
            色空間の変換．
            '''
            try:
                if converter["params"]["mode"] not in CV2CvtColorMode.members():
                    raise ValueError("Not found mode in 'CV2CvtColorMode'.")
                frame = cv2.cvtColor(frame, converter["params"]["mode"].cv2_constant)
            except Exception as e:
                raise type(e)("Failed in '{mode}'. Detail: {err}".format(
                    mode = converter["params"]["mode"].name,
                    err = traceback.format_exception_only(type(e), e)[0]))
        if converter["method"] == ImgConvertMethod.BLUR_AVG:
            '''
            平滑化(平均フィルタ)．
            '''
            frame = cv2.blur(
                frame,
                (converter["params"]["width"], converter["params"]["height"]))
        if converter["method"] == ImgConvertMethod.BLUR_MED:
            '''
            平滑化(中央値フィルタ)．
            '''
            frame = cv2.medianBlur(
                frame,
                converter["params"]["size"])
        if converter["method"] == ImgConvertMethod.BLUR_GAUSSIAN:
            '''
            平滑化(ガウシアンフィルタ)．
            '''
            frame = cv2.GaussianBlur(
                frame,
                (converter["params"]["width"], converter["params"]["height"]),
                converter["params"]["sigma_x"])
        if converter["method"] == ImgConvertMethod.BLUR_BILATERAL:
            '''
            平滑化(バイラテラルフィルタ)．
            '''
            frame = cv2.bilateralFilter(
                frame,
                converter["params"]["size"],
                converter["params"]["sigma_color"],
                converter["params"]["sigma_space"])
        if converter["method"] == ImgConvertMethod.INVERT:
            '''
            反転．
            '''
            frame = cv2.bitwise_not(frame)
        if converter["method"] == ImgConvertMethod.THRESHOLD:
            '''
            2値化．
            '''
            try:
                if converter["params"]["mode"] not in CV2ThresholdMode.members():
                    raise ValueError("Not found mode in 'CV2ThresholdMode'.")
                _, frame = cv2.threshold(
                    frame,
                    converter["params"]["threshold"],
                    255,
                    converter["params"]["mode"].cv2_constant)
            except Exception as e:
                raise type(e)("Failed in '{mode} threshold'. Detail: {err}".format(
                    mode = converter["params"]["mode"].name,
                    err = traceback.format_exception_only(type(e), e)[0]))
        if converter["method"] == ImgConvertMethod.BGR_SAT_BRT:
            '''
            BGR色空間に対する彩度・明度補正．
            '''
            frame = cv2_bgr_saturation(frame, converter["params"]["ratio_sat"])
            frame = cv2_bgr_brightness(frame, converter["params"]["ratio_brt"])
        if converter["method"] == ImgConvertMethod.BGR_GAMMA_GRAY:
            '''
            BGR色空間に対するガンマ補正・低輝度対応のグレースケール(より色の区別つけやすくしてる？)
            '''
            frame = cv2_bgr_gamma_gray_scale(frame, scale = 2.2, ret_uint8 = True)
        if converter["method"] == ImgConvertMethod.CVTGAMMA:
            '''
            ガンマ補正．
            '''
            try:
                if converter["params"]["mode"] not in CV2CvtGammaMode.members():
                    raise ValueError("Not found mode in 'CV2CvtGammaMode'.")
                if converter["params"]["mode"] == CV2CvtGammaMode.INV_NEGAPOSI:
                    frame = cv2_gamma_inv_negaposi(frame)
                if converter["params"]["mode"] == CV2CvtGammaMode.BINARIZE:
                    frame = cv2_gamma_binarize(frame, converter["params"]["gamma"])
                if converter["params"]["mode"] == CV2CvtGammaMode.POSTARIZE:
                    frame = cv2_gamma_postarize(frame, converter["params"]["gamma"])
                if converter["params"]["mode"] == CV2CvtGammaMode.SOLARIZE:
                    frame = cv2_gamma_solarize(frame)
                if converter["params"]["mode"] == CV2CvtGammaMode.BRIGHTNESS:
                    frame = cv2_gamma_brightness(frame, converter["params"]["gamma"])
            except Exception as e:
                raise type(e)("Failed in '{mode}. Detail: {err}".format(
                    mode = converter["params"]["mode"].name,
                    err = traceback.format_exception_only(type(e), e)[0]))
        if converter["method"] == ImgConvertMethod.DECOLOR:
            '''
            退色処理
            '''
            frame, _ = cv2.decolor(frame)
        if converter["method"] == ImgConvertMethod.MOSAIC:
            '''
            モザイク
            '''
            frame = cv2_mosaic(frame, converter["params"]["ratio"])
        
        if display_progress_imgs:
            fig = plt.figure(figsize = (20, 10))
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.imshow(base_frame, vmin = 0, vmax = 255, cmap = "gray")
            ax1.set_title("Input")
            ax2 = fig.add_subplot(1, 2, 2)
            ax2.imshow(frame, vmin = 0, vmax = 255, cmap = "gray")
            ax2.set_title("{curr}/{all}: After {method}".format(
                curr = conv_i + 1,
                all = len(converters),
                method = converter["method"].name
            ))
            plt.show()

    if path_result is not None:
        cv2.imwrite(path_result, frame)
    return frame



class ImgConvertMethod(Enum):
    SCALE = "scale"
    RESIZE = "resize"
    CVTCOLOR = "cvtColor"
    BLUR_AVG = "blur_average"
    BLUR_MED = "blur_median"
    BLUR_GAUSSIAN = "blur_gaussian"
    BLUR_BILATERAL = "blur_bilateral"
    INVERT = "invert"
    THRESHOLD = "threshold"
    BGR_SAT_BRT = "bgr_saturation_brightness"
    BGR_GAMMA_GRAY = "bgr_gamma_gray_scale"
    CVTGAMMA = "cvtGamma" # ガンマ補正
    DECOLOR = "decolor"
    MOSAIC = "mosaic"
    def __init__(self, label):
        self.label = label

    @staticmethod
    def members():
        return [*ImgConvertMethod.__members__.values()]

class CV2CvtColorMode(Enum):
    RGB2BGR = ("rgb2bgr", cv2.COLOR_RGB2BGR)
    RGB2GRAY = ("rgb2gray", cv2.COLOR_RGB2GRAY)
    RGB2XYZ = ("rgb2xyz", cv2.COLOR_RGB2XYZ)
    RGB2YCC = ("rgb2ycc", cv2.COLOR_RGB2YCrCb)
    RGB2HSV = ("rgb2hsv", cv2.COLOR_RGB2HSV)
    RGB2HLS = ("rgb2hls", cv2.COLOR_RGB2HLS)
    RGB2LAB = ("rgb2lab", cv2.COLOR_RGB2Lab)
    RGB2LUV = ("rgb2luv", cv2.COLOR_RGB2Luv)
    BGR2RGB = ("bgr2rgb", cv2.COLOR_BGR2RGB)
    BGR2GRAY = ("bgr2gray", cv2.COLOR_BGR2GRAY)
    BGR2XYZ = ("bgr2xyz", cv2.COLOR_BGR2XYZ)
    BGR2YCC = ("bgr2ycc", cv2.COLOR_BGR2YCrCb)
    BGR2HSV = ("bgr2hsv", cv2.COLOR_BGR2HSV)
    BGR2HLS = ("bgr2hls", cv2.COLOR_BGR2HLS)
    BGR2LAB = ("bgr2lab", cv2.COLOR_BGR2Lab)
    BGR2LUV = ("bgr2luv", cv2.COLOR_BGR2Luv)
    GRAY2RGB = ("rgb2gray", cv2.COLOR_GRAY2RGB)
    GRAY2BGR = ("rgb2gray", cv2.COLOR_GRAY2BGR)
    def __init__(self, label, cv2_constant):
        self.label = label
        self.cv2_constant = cv2_constant
    
    @staticmethod
    def members():
        return [*CV2CvtColorMode.__members__.values()]

# class CV2BlurMode(Enum):
#     '''
#     - Refs
#         - http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_filtering/py_filtering.html
#         - https://qiita.com/shoku-pan/items/07ec25f1d50629fed698
#         - https://qiita.com/ankomotch/items/74884b0ca24b739159c0
#     '''
#     AVG = "average"
#     MED = "median"
#     GAUSSIAN = "gaussian"
#     BILATERAL = "bilateral"
#     def __init__(self, label):
#         self.label = label

#     @staticmethod
#     def members():
#         return [*CV2BlurMode.__members__.values()]

class CV2ThresholdMode(Enum):
    BINARY = ("binary", cv2.THRESH_BINARY)
    BINARY_INV = ("binary_inv", cv2.THRESH_BINARY_INV)
    TRUNC = ("trunc", cv2.THRESH_TRUNC)
    TOZERO = ("tozero", cv2.THRESH_TOZERO)
    TOZERO_INV = ("tozero_inv", cv2.THRESH_TOZERO_INV)
    def __init__(self, label, cv2_constant):
        self.label = label
        self.cv2_constant = cv2_constant
    
    @staticmethod
    def members():
        return [*CV2ThresholdMode.__members__.values()]

class CV2CvtGammaMode(Enum):
    '''
    - Refs
        - https://pystyle.info/opencv-tone-transform/
        - https://qiita.com/shoku-pan/items/0e2284f6b53e1b3f40f8
    '''
    INV_NEGAPOSI = "invert_negative_positive"
    BINARIZE = "binarize"
    POSTARIZE = "postarize"
    SOLARIZE = "solarize"
    BRIGHTNESS = "brightness"
    def __init__(self, label):
        self.label = label

    @staticmethod
    def members():
        return [*CV2CvtGammaMode.__members__.values()]




def cv2_bgr_saturation(frame, ratio):
    '''
    - Refs
        - https://tat-pytone.hatenablog.com/entry/2019/04/14/193237
    '''
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame[:, :, 1] = frame[:, :, 1] * ratio
    return cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

def cv2_bgr_brightness(frame, ratio):
    '''
    - Refs
        - https://tat-pytone.hatenablog.com/entry/2019/04/14/193237
    '''
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame[:, :, 2] = frame[:, :, 2] * ratio
    return cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

def cv2_bgr_gamma_gray_scale(frame, scale = 2.2, ret_uint8 = False):
    '''
    - Args
        - frame:cv2:
        - scale:float:
        - ret_uint8:bool: np.uint8に変換して返すか．内部ではfloat32で計算して低輝度を拾えるようにしているが，後続の画像処理で扱えない場合がある．ただnp.uint8にすると低輝度を結局潰してしまう可能性あり．
    - Refs
        - https://qiita.com/yoya/items/dba7c40b31f832e9bc2a#opencv-%E3%81%A7%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB%E5%8C%96-%E3%82%AC%E3%83%B3%E3%83%9E%E8%A3%9C%E6%AD%A3%E4%BD%8E%E8%BC%9D%E5%BA%A6%E5%AF%BE%E5%BF%9C
    '''
    lut = np.array(
        [pow(x / 255.0, scale) for x in range(256)],
        dtype = "float32"
    )
    frame = cv2.LUT(frame, lut)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = pow(frame, 1.0 / scale) * 255
    if ret_uint8:
        frame = frame.astype(np.uint8)
    return frame

def cv2_gamma_inv_negaposi(frame):
    '''
    - Refs
        - https://pystyle.info/opencv-tone-transform/
    '''
    x = np.arange(256)
    lut = 255 - x
    return cv2.LUT(frame, lut)

def cv2_gamma_binarize(frame, threshold):
    '''
    gamma = threshold．
    - Refs
        - https://pystyle.info/opencv-tone-transform/
    '''
    x = np.arange(256)
    lut = np.where(x <= threshold, 0, 255)
    return cv2.LUT(frame, lut)

def cv2_gamma_postarize(frame, steps):
    '''
    gamma = steps．
    - Refs
        - https://pystyle.info/opencv-tone-transform/
        - https://www.gesource.jp/weblog/?p=8244
    '''
    x = np.arange(256)
    bins = np.linspace(0, 255, steps + 1)
    lut = np.array(
        [bins[i - 1] for i in np.digitize(x, bins)]
    ).astype(int)
    return cv2.LUT(frame, lut)

def cv2_gamma_solarize(frame):
    x = np.arange(256)
    lut = (np.sin(x * 2 * np.pi / 255) + 1) * 255 / 2
    return cv2.LUT(frame, lut)

def cv2_gamma_brightness(frame, gamma):
    '''
    - Refs
        - https://qiita.com/shoku-pan/items/0e2284f6b53e1b3f40f8
    '''
    lut = np.zeros((256, 1), dtype = np.uint8)
    for i in range(256):
        lut[i][0] = 255 * (float(i) / 255) ** (1.0 / gamma)
    return cv2.LUT(frame, lut)

def cv2_mosaic(frame, ratio):
    width = frame.shape[1]
    height = frame.shape[0]
    return cv2.resize(
        cv2.resize(frame, dsize = None, fx = ratio, fy = ratio),
        dsize = (width, height)
    )



def cv2_np2base64(frame):
    _, data = cv2.imencode(".jpg", frame)
    return base64.b64encode(data)

def cv2_base642np(base64_img):
    bytes_img = base64.b64decode(base64_img)
    np_img = np.fromstring(bytes_img, np.uint8)
    return cv2.imdecode(np_img, cv2.IMREAD_ANYCOLOR) # cv2.IMREAD_UNCHANGED # cv2.IMREAD_COLOR