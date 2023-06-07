# Azure OCR (Cognitive Service Read API v3.2) を使って、画像から文字を読み取る

https://qiita.com/c-makitahiroki/items/e3e4a52eb2b92a15fd22

以上の記事を参考に実施。

## 実行環境
Python 3.9.6

## ライブラリのインストール

```
pip3 install -r requirements.txt
```
python-dotenvとtqdmしか利用していないので、独自にインストールしていても大丈夫。

## Azure Potal での設定と.envの設定
[https://portal.azure.com/](https://portal.azure.com/) にて、Azure OCR のサブスクリプションを作成して
Computer Visionのリソースを作成する。キーとエンドポイントより、 `.env` ファイルに以下を設定。

```
AZURE_SUBSCRIPTION_KEY={キー1の内容}
AZURE_ENDPOINT={エンドポイントの内容}
```

# 実行

これで実行。`target` フォルダに入っている結果のJSONファイルが `output_json` に出力される。

```
python3 main.py
```

なおさらにJSONのOCRの結果をただのテキストにしたものを取得したい場合には、以下を実行すると `output_text` にテキストファイルが出力される。

```
python3 json-processer.py
```


