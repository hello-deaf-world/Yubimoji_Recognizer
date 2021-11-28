import numpy as np

# def get_dist_hamming

# def get_dist_levenshtein

# def get_dist_jaro


def get_dist_cos(np1, np2):
    '''
    1次元numpy配列間のコサイン類似度を求めて返す．
    多次元numpy配列の場合は1次元numpy配列にflattenしてから渡すこと．
    '''
    return np.dot(np1, np2) / (np.linalg.norm(np1) * np.linalg.norm(np2))