# Azure OCR (Cognitive Service Read API v3.2) を使って、画像から文字を読み取る

https://qiita.com/c-makitahiroki/items/e3e4a52eb2b92a15fd22

以上の記事を参考に実施。

## 実行環境
Python 3.9.6

## ライブラリのインストール

```
pip3 install -r requirements.txt
```
python-dotenv しか利用していないので、独自にインストールしていても大丈夫。

## Azure Potal での設定と.envの設定
[https://portal.azure.com/](https://portal.azure.com/) にて、Azure OCR のサブスクリプションを作成して
Computer Visionのリソースを作成する。キーとエンドポイントより、 `.env` ファイルに以下を設定。

```
AZURE_SUBSCRIPTION_KEY={キー1の内容}
AZURE_ENDPOINT={エンドポイントの内容}
```

# 実行

これで実行。

```
python3 main.py
```
