class MPMarkerTrace:
    '''
    mediapileのある指定したマーカー個別の動作履歴を保持するクラス．
    '''
    def __init__(self,
        target_markers,
        len_history = 16,):