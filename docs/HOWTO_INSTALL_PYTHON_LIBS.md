# Pythonライブラリのインストール方法メモ
### torch/torchvision/torchaudio/torchtext等
1. 下記要件を事前確認する．
    - Python開発・実行する環境のOS
    - CPU/GPUのどっちで実行するか
    - Pythonバージョン
    - torchのバージョンとそれに互換のあるtorchvision等のバージョン
2. [https://download.pytorch.org/whl/cpu/torch_stable.html](https://download.pytorch.org/whl/cpu/torch_stable.html)にアクセス．
3. 1.で確認した要件を満たす`.whl`を探し，リンクをコピーする．
4. 下記コマンドを実行してpipインストール
    ```
    $ pip install {3.でコピーしたwhlのリンク}
    ```
