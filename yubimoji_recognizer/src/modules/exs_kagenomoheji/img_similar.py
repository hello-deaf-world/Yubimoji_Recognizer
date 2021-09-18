import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
from modules.exs_kagenomoheji.img_converter import (
    selective_convert_img,
    ImgConvertMethod,
    CV2CvtColorMode
)
from modules.exs_kagenomoheji.distance import (
    get_dist_cos
)


# def find_similar_imgfiles(base_img_path, target_dir, display_compare = False):


# def get_imgfile_ahash



# def get_imgfile_dhash



# def get_imgfile_dhash





'''
# 画像類似度の手法
- ヒストグラム比較
    - 色合いで比較
        - 「どの色がどれだけ発生しているか」をヒストグラムとして見ている？
        - 色が発生している場所は考慮されてなさそう
    - 関数compare_color_histgramsを実装したのでそれを使用して．


# find_similar_imgfiles関数について実装予定
1. 複数の類似度手法を選択できるようにリスト型引数を用意する
2. 選択された類似度手法だけ類似度を個別に求める
3. 各スコアに対し，下記で総合スコアを求めてみる
    - 正規化または標準化して合計点を求める
        - https://www.codexa.net/normalization-python/
        - https://www.hobby-happymylife.com/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0/normalization_zscore/
    - 偏差値を求める
        - https://qiita.com/kenmatsu4/items/e6c6acb289c02609e619#6%E4%BE%8B2%E5%81%8F%E5%B7%AE%E5%80%A4
'''

def compare_color_histgrams(
    path_base_img = None,
    np_base_img = None,
    path_comp_img = None,
    np_comp_img = None,
    resize = (200, 200),
    display_histgrams = False):
    '''
    カラーヒストグラムによる類似度を返す．
    比較する2画像のサイズを引数resizeのサイズに揃えた後，各々のカラーヒストグラムを求めて比較することが推奨．

    - Args
        - path_base_img:str: 
        - np_base_img:np.array: 
        - path_comp_img:str: 
        - np_comp_img:np.array: 
        - resize:(width:int, height:int): 
    - Returns
        - カラーヒストグラムによる類似度
    -Refs
        - https://qiita.com/best_not_best/items/c9497ffb5240622ede01#%E6%A4%9C%E8%A8%BC1-%E3%83%92%E3%82%B9%E3%83%88%E3%82%B0%E3%83%A9%E3%83%A0%E6%AF%94%E8%BC%83
            - ここにあるヒストグラム比較では，関数cv2.calcHistの第2引数で「[0]」としか指定していないのでblue色空間しか見れてないのでは？
        - https://code-graffiti.com/histograms-with-opencv-in-python/
        - https://pystyle.info/opencv-histogram/
        - https://theailearner.com/tag/cv2-comparehist/
    
    TODO: カラーヒストグラムの導出など内部関数を外部化する
    '''
    frame_base = None
    frame_comp = None
    if (frame_base is None) and (path_base_img is not None):
        frame_base = cv2.imread(path_base_img)
    if (frame_base is None) and (np_base_img is not None):
        frame_base = deepcopy(np_base_img)
    if frame_base is None:
        raise ValueError("Empty in variable 'frame_base'.")
    if (frame_comp is None) and (path_comp_img is not None):
        frame_comp = cv2.imread(path_comp_img)
    if (frame_comp is None) and (np_comp_img is not None):
        frame_comp = deepcopy(np_comp_img)
    if frame_comp is None:
        raise ValueError("Empty in variable 'frame_comp'.")
    
    def __pre_cv2_convert(np_frame):
        cv2_methods = [
            {
                # cv2.imreadでBGRまたはBGRAと見なされてしまうので，まず戻す必要あり(不要かも)
                "method": ImgConvertMethod.CVTCOLOR,
                "params": {
                    "mode": CV2CvtColorMode.BGR2RGB
                }
            },
            {
                "method": ImgConvertMethod.RESIZE,
                "params": {
                    "width": resize[0],
                    "height": resize[1]
                }
            },
        ]
        return selective_convert_img(
            cv2_methods,
            np_img = np_frame)
    frame_base = __pre_cv2_convert(frame_base)
    frame_comp = __pre_cv2_convert(frame_comp)

    def __get_color_histgrams(np_frame, channels = [0, 1, 2]):
        '''
        指定したchannelsだけの色のヒストグラムを求め，2次元numpy配列(cv2.calcHist関数の戻り値の形式的に厳密には3次元になってるが)として格納して返す．
        - Args
        - Returns
        - Memo
            - cv2.calcHist()のchannelsの数字は，BGR=012になってるらしい？
        '''
        hists = []
        for ch in channels:
            hists.append(
                cv2.calcHist(
                    [np_frame],
                    channels = [ch],
                    mask = None,
                    histSize = [256], # bin数
                    ranges = [0, 256])
            )
        return np.array(hists)
    hists_base = __get_color_histgrams(frame_base)
    hists_comp = __get_color_histgrams(frame_comp)
    # print(hists_base.shape)
    # print(hists_comp.shape)

    def __display_hists(
        np_frame_base,
        hists_base,
        np_frame_comp,
        hists_comp):
        CHANNELS = ["b", "g", "r"] # cv2.calcHist()のchannelsの順序的にこれっぽい
        fig = plt.figure(figsize = (20, 10))
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.imshow(np_frame_base, vmin = 0, vmax = 255, cmap = "gray")
        ax1.set_title("base")
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.imshow(np_frame_comp, vmin = 0, vmax = 255, cmap = "gray")
        ax2.set_title("comp")
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        for i, ch in enumerate(CHANNELS):
            ax3.plot(hists_base[i], color = ch)
            ax4.plot(hists_comp[i], color = ch)
        plt.show()
    if display_histgrams:
        __display_hists(
            frame_base,
            hists_base,
            frame_comp,
            hists_comp)

    # print(cv2.compareHist(hists_base, hists_comp, 0))
    # print(get_dist_cos(hists_base.ravel(), hists_comp.ravel()))
    return cv2.compareHist(hists_base, hists_comp, 0)

